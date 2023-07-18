import psycopg2
import configparser

def delete_user_database(email):
    params = {
        "host": '10.1.20.252',
        "port": 5432,
        "database": 'ERP_EIPSA',
        "user": 'postgres',
        "password": 'EIPS@0545$@!'
    }
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    command_check_user = ("""
                        SELECT * FROM registration
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
