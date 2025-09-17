import psycopg2

class Database_Connection():
    def __init__(self, config):
        self.config = config
        self.connection = None

    def __enter__(self):
        self.connection = psycopg2.connect(**self.config)
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.connection:
            self.connection.close()