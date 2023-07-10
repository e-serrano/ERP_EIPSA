import psycopg2
import configparser

def create_user_database(username,password):
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

    command_create_user = f"CREATE USER \"{username}\" WITH PASSWORD '{password}'"
    commands_privileges = """
        GRANT INSERT, SELECT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO "{}";
        GRANT TRUNCATE ON ALL TABLES IN SCHEMA public TO "{}";
        GRANT REFERENCES ON ALL TABLES IN SCHEMA public TO "{}";
        GRANT TRIGGER ON ALL TABLES IN SCHEMA public TO "{}";
        GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO "{}";
        GRANT INSERT, SELECT, UPDATE, DELETE ON ALL TABLES IN SCHEMA logging TO "{}";
        GRANT TRUNCATE ON ALL TABLES IN SCHEMA logging TO "{}";
        GRANT REFERENCES ON ALL TABLES IN SCHEMA logging TO "{}";
        GRANT TRIGGER ON ALL TABLES IN SCHEMA logging TO "{}";
        GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA logging TO "{}";
    """.format(username, username, username, username, username, username, username, username, username, username)

    # Create user
    cur.execute(command_create_user)

    # Grant privileges
    cur.execute(commands_privileges)

    conn.commit()

    # Close connection
    cur.close()
    conn.close()