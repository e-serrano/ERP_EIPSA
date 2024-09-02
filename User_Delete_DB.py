import psycopg2
from config import config

def delete_user_database(email):
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
    commands_delete_privileges = """
        REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA logging FROM "{}";
        REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM "{}";
        REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM "{}";
        REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA logging FROM "{}";
        DROP USER  "{}";
    """.format(user_db, user_db, user_db, user_db, user_db)

    cur.execute(commands_delete_privileges)

    conn.commit()

    # Close connection
    cur.close()
    conn.close()
