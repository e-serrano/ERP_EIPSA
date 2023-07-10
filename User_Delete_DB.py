import psycopg2
import configparser

def delete_user_database(email):
    config_obj = configparser.ConfigParser()
    config_obj.read("database_master.ini")
    dbparam = config_obj["postgresql"]
    # set your parameters for the database connection URI using the keys from the configfile.ini
    host_database = dbparam["host"]
    name_database = dbparam["database"]
    user_database = dbparam["user"]
    password_database = dbparam["password"]
    params = {
        "host": host_database,
        "port": 5432,
        "database": name_database,
        "user": user_database,
        "password": password_database
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
