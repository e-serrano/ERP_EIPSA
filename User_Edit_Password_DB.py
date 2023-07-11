import psycopg2
import configparser

def edit_user_password_database(username,new_password):
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

    command_create_user = f"ALTER USER \"{username}\" WITH PASSWORD '{new_password}'"

# Edit password
    cur.execute(command_create_user)

    conn.commit()

# Close connection
    cur.close()
    conn.close()

# editing the database.ini file for each user
    edit = configparser.ConfigParser()
    edit.read("database.ini")
# Get the postgresql section
    postgresql = edit["postgresql"]
# Update the user and password
    postgresql["password"] = new_password
# Write changes back to file
    with open('database.ini', 'w') as configfile:
        edit.write(configfile)