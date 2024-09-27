import psycopg2
from config import config

def delete_user_database(email):
    """
    Deletes a user from the database based on the provided email.

    Args:
        email (str): The email of the user to be deleted.
    """
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    command_check_user = ("""
                        SELECT * FROM users_data.registration
                        WHERE "email" = %s
                        """)

    # Check username with email 
    cur.execute(command_check_user, (email,))
    results=cur.fetchall()
    match=list(filter(lambda x:email in x, results))
    user_db=match[0][3]

    # Revoke all privileges and delete user from database
    cur.execute("""
        SELECT nspname FROM pg_catalog.pg_namespace;
    """)
    schemas = cur.fetchall()

    commands_delete_privileges = []

    for schema in schemas:
        schema_name = schema[0]
        commands_delete_privileges.append(f"REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA {schema_name} FROM \"{user_db}\";")
        commands_delete_privileges.append(f"REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA {schema_name} FROM \"{user_db}\";")

    commands_delete_privileges.append(f"REVOKE ALL PRIVILEGES ON DATABASE \"ERP_EIPSA\" FROM \"{user_db}\";")
    commands_delete_privileges.append(f"DROP USER \"{user_db}\";")

    for command in commands_delete_privileges:
        cur.execute(command)

    conn.commit()

    # Close connection
    cur.close()
    conn.close()
