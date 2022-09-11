from result_finder import ResultFinder
import os
import pandas as pd

class DataframeAnalysis:

    def __init__(self):

        self.result_finder = ResultFinder()

    def get_dataframe(self, football_league: str, year: int):
        
        result: str = self.result_finder.get_results(football_league, year)
            
        try:

            df = pd.read_csv(fr"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results/{football_league}/{result}")

            return df

        except FileNotFoundError:

            print("The football league or annual results cannot be found. Please check the league name is correct or year is correct.")

    def get_list_of_teams(self, football_league: str, year: int = None) -> list:

        try:

            if year == None: # Gets list of teams in the whole league over all years
                
                self.result_finder.go_to_football_league(football_league)

                annual_results: list[str] = os.listdir(".")

                list_of_teams_with_duplicates: list[str] = []

                for annual_result in annual_results:

                    df = pd.read_csv(annual_result)

                    teams = list(df["Home_Team"])

                    list_of_teams_with_duplicates.extend(teams)

                list_of_teams = set(list_of_teams_with_duplicates)

                return list_of_teams

            else:
                
                annual_result = self.result_finder.get_results(football_league, year)

                df = pd.read_csv(annual_result)

                teams = list(df["Home_Team"])
                
                list_of_teams = set(teams)

                return(list_of_teams)

        except FileNotFoundError:

            print("Football league doesn't exist or there are no records.")

        except ValueError:

            print("No results for the specified year")

    
    def get_number_of_teams(self, football_league: str, year: int = None):

        list_of_teams: list[str] = self.get_list_of_teams(football_league, year)

        try:
            
            return len(list_of_teams)

        except:

            print("No record for this league")

    def get_winner(self, football_league: str, year: int, home_team: str, away_team: str) -> str:

        df = self.get_dataframe(football_league, year) # returns df

        data = df[(df["Home_Team"] == home_team) & (df["Away_Team"] == away_team)]

        for index, row in data.iterrows():
            
            result: str = row["Result"]
            home_team_score = int(result[0])
            away_team_score = int(result[2])

            if home_team_score > away_team_score:

                return home_team

            elif home_team_score < away_team_score:

                return away_team

            else:

                return "draw"

    
    def get_number_of_home_wins(self, football_league: str, year: int, team):

        df = self.get_dataframe(football_league, year)

        data = df[df["Home_Team"] == team]

        home_wins: int = 0

        for index, row in data.iterrows():

            result: str = row["Result"]
            home_team_score = int(result[0])
            away_team_score = int(result[2])

            if home_team_score > away_team_score:

                home_wins += 1

        return home_wins



            
        


if __name__ == "__main__":

    dataframe = DataframeAnalysis()
    print(dataframe.get_number_of_home_wins("premier_league", 2021, "Tottenham Hotspur"))