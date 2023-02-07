import psycopg

class Con:
    def __init__(self, dbname, user, password, host):
        self.connection_string = f"dbname={dbname} user={user} password={password} host={host}"

    def create(self, *args) -> psycopg.Connection:
        """Create a postgres connection.
        """
        return psycopg.connect(self.connection_string, *args)
