from result_finder import ResultFinder
import os
import pandas as pd

class DataframeAnalysis:

    def __init__(self):

        self.result_finder = ResultFinder()
        self.INDEX_OF_AWAY_TEAM = 2


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
            away_team_score = int(result[self.INDEX_OF_AWAY_TEAM])

            if home_team_score > away_team_score:

                return home_team

            elif home_team_score < away_team_score:

                return away_team

            else:

                return "draw"

    
    def get_home_wins(self, football_league: str, year: int, team: str) -> int:

        df = self.get_dataframe(football_league, year)

        data = df[df["Home_Team"] == team]

        home_wins: int = 0

        for index, row in data.iterrows():

            result: str = row["Result"]
            home_team_score = int(result[0])
            away_team_score = int(result[self.INDEX_OF_AWAY_TEAM])

            if home_team_score > away_team_score:

                home_wins += 1

        return home_wins

    
    def get_away_wins(self, football_league: str, year: int, team: str) -> int:

        df = self.get_dataframe(football_league, year)

        data = df[df["Away_Team"] == team]

        away_wins: int = 0

        for index, row in data.iterrows():

            result: str = row["Result"]
            home_team_score = int(result[0])
            away_team_score = int(result[self.INDEX_OF_AWAY_TEAM])

            if home_team_score < away_team_score:

                away_wins += 1

        return away_wins


    def get_total_wins(self, football_league: str, year: int, team: str):

        home_wins: int = self.get_home_wins(football_league, year, team)
        away_wins: int = self.get_away_wins(football_league, year, team)

        total_wins: int = home_wins + away_wins

        return total_wins

    def get_total_win_since_beginning(self, football_league: str, team: str) -> int:

        list_of_years: list[int] = self.result_finder.get_list_of_years(football_league)

        total_wins_over_all_years: int = 0

        for year in list_of_years:

            total_wins: int = self.get_total_wins(football_league, year, team)

            total_wins_over_all_years += total_wins

        return total_wins_over_all_years


    def get_leaderboard(self, football_league: str, year: int) -> dict:

        list_of_teams: list[str] = self.get_list_of_teams(football_league, year)

        win_count_dictionary: dict[str:str] = {}
    
        for team in list_of_teams:

            total_wins: int = self.get_total_wins(football_league, year, team)

            win_count_dictionary[team] = total_wins

        return dict(sorted(win_count_dictionary.items(), key=lambda x:x[1], reverse=True))

    
    def get_all_leaderboards(self, football_league: str) -> list:

        list_of_years: list[int] = self.result_finder.get_list_of_years(football_league)

        dictionary_of_year_to_leaderboard: dict = {} 
        list_of_leaderboards: list[dict[str:int]] = []

        for year in list_of_years:

            leaderboard: dict[str:int] = self.get_leaderboard(football_league, year)

            dictionary_of_year_to_leaderboard[year] = leaderboard

            list_of_leaderboards.append(dictionary_of_year_to_leaderboard)

        return list_of_leaderboards

    
    def get_all_time_leaderboard(self, football_league: str) -> dict:

        list_of_teams: list[str] = self.get_list_of_teams(football_league)

        win_count_dictionary: dict[str:str] = {}

        for team in list_of_teams:

            total_wins: int = self.get_total_win_since_beginning(football_league, team)

            win_count_dictionary[team] = total_wins

        return dict(sorted(win_count_dictionary.items(), key=lambda x:x[1], reverse=True))


if __name__ == "__main__":

    dataframe = DataframeAnalysis()
    print(dataframe.get_all_time_leaderboard("premier_league"))