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

    
    def get_all_records(self) -> list:

        df = self.dataframe.make_dataframe()

        all_records: list[tuple[str,int]] = []

        for _, row in df.iterrows():

            record = tuple(row)

            all_records.append(record)

        return all_records


    def upload_to_table(self, host: str, user: str, password: str, dbname: str, port: int):

        all_records: list[tuple[str,int]] = self.get_all_records()

        for record in all_records:

            sql_code: str = f"""
            INSERT INTO football_data (teams, wins, streaks, goals)
            VALUES {record}
            """

            self.execute_to_postgres(host, user, password, dbname, port, sql_code)


    def show_table(self, host: str, user: str, password: str, dbname: str, port: int):

        sql_code: str = """SELECT * FROM football_data"""

        self.execute_to_postgres(host, user, password, dbname, port, sql_code)
    
