from football_dataframe import FootballDataframe
import psycopg2

class Database:

    def __init__(self, football_league: str):

        self.dataframe = FootballDataframe(football_league)

    
    def execute_to_postgres(self, host: str, user: str, password: str, dbname: str, port: int, sql_code: str):

        with psycopg2.connect(host = host, user = user, password = password, dbname = dbname, port = port) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_code)


    def create_table(self, host: str, user: str, password: str, dbname: str, port: int):

        sql_code: str = """
        DROP TABLE IF EXISTS football_data; CREATE
        TABLE football_data (
            teams       VARCHAR,
            wins        INTEGER,
            streaks     INTEGER,
            goals       INTEGER
        );
        
        """
        
        self.execute_to_postgres(host, user, password, dbname, port, sql_code)

    
    def give_sql_input(self):

        pass


if __name__ == "__main__":

    HOST: str = "football.cqav9sfxcwg5.eu-west-2.rds.amazonaws.com"
    USER: str = "postgres"
    PASSWORD: str = "Jguan2001"
    DBNAME: str = "postgres"
    PORT: int = 5432

    database = Database("premier_league")
    database.create_table(HOST, USER, PASSWORD, DBNAME, PORT)

    

    