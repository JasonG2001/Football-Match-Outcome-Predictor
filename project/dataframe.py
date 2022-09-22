from result_finder import ResultFinder
import os
import pandas as pd
import pickle

class DataframeAnalysis:

    def __init__(self, football_league: str):

        self.football_league: str = football_league
        self.result_finder = ResultFinder(football_league)
        self.INDEX_OF_AWAY_TEAM = 2


    def get_dataframe(self, year: int):
        
        result: str = self.result_finder.get_results(year)
            
        try:

            df = pd.read_csv(fr"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results/{self.football_league}/{result}")

            return df

        except FileNotFoundError:

            print("The football league or annual results cannot be found. Please check the league name is correct or year is correct.")


    def get_elo(self) -> dict:

        elo = pickle.load(open('/home/jason2001/Football-Match-Outcome-Predictor/project/elo_dict.pkl', 'rb'))

        return elo


    def get_list_of_teams(self, year: int = None) -> list:

        try:

            if year == None: # Gets list of teams in the whole league over all years
                
                self.result_finder.go_to_football_league()

                annual_results: list[str] = os.listdir(".")

                list_of_teams_with_duplicates: list[str] = []

                for annual_result in annual_results:

                    df = pd.read_csv(annual_result)

                    teams = list(df["Home_Team"])

                    list_of_teams_with_duplicates.extend(teams)

                list_of_teams = set(list_of_teams_with_duplicates)

                return list_of_teams

            else:
                
                annual_result = self.result_finder.get_results(year)

                df = pd.read_csv(annual_result)

                teams = list(df["Home_Team"])
                
                list_of_teams = set(teams)

                return(list_of_teams)

        except FileNotFoundError:

            print("Football league doesn't exist or there are no records.")

        except ValueError:

            print("No results for the specified year")

    
    def get_number_of_teams(self, year: int = None):

        list_of_teams: list[str] = self.get_list_of_teams(year)

        try:
            
            return len(list_of_teams)

        except:

            print("No record for this league")


    def get_winner(self, year: int, home_team: str, away_team: str) -> str:

        df = self.get_dataframe(year) # returns df

        data = df[(df["Home_Team"] == home_team) & (df["Away_Team"] == away_team)]

        result = data.loc[:, "Result"]

        for i, score in enumerate(result):
            
            home_team_score = int(score[0])
            away_team_score = int(score[self.INDEX_OF_AWAY_TEAM])

            if home_team_score > away_team_score:

                return home_team

            elif home_team_score < away_team_score:

                return away_team

            else:

                return "draw"

    
    def get_home_wins(self, year: int, team: str) -> int:

        df = self.get_dataframe(year)

        data = df[df["Home_Team"] == team]

        home_wins: int = 0

        result = data.loc[:, "Result"]

        for i, score in enumerate(result):

            home_team_score = int(score[0])
            away_team_score = int(score[self.INDEX_OF_AWAY_TEAM])

            if home_team_score > away_team_score:

                home_wins += 1

        return home_wins

    
    def get_away_wins(self, year: int, team: str) -> int:

        df = self.get_dataframe(year)

        data = df[df["Away_Team"] == team]

        away_wins: int = 0

        result = data.loc[:, "Result"]

        for i, score in enumerate(result):

            home_team_score = int(score[0])
            away_team_score = int(score[self.INDEX_OF_AWAY_TEAM])

            if home_team_score < away_team_score:

                away_wins += 1

        return away_wins


    def get_total_wins(self, year: int, team: str) -> int:

        home_wins: int = self.get_home_wins(year, team)
        away_wins: int = self.get_away_wins(year, team)

        total_wins: int = home_wins + away_wins

        return total_wins


    def get_home_total_points(self, year: int, team: str) -> int:

        df = self.get_dataframe(year)

        new_df = df[df["Home_Team"] == team]

        home_points: int = 0

        result = new_df.loc[:, "Result"]

        for i, score in enumerate(result):

            goals = int(score[0])

            home_points += goals

        return home_points


    def get_away_total_points(self, year: int, team: str) -> int:

        df = self.get_dataframe(year)

        new_df = df[df["Away_Team"] == team]

        away_points: int = 0

        result = new_df.loc[:, "Result"]

        for i, score in enumerate(result):

            goals = int(score[self.INDEX_OF_AWAY_TEAM])

            away_points += goals

        return away_points


    def get_total_points(self, year: int, team: str) -> int:

        home_points: int = self.get_home_total_points(year, team)
        away_points: int = self.get_away_total_points(year, team)

        total_points: int = home_points + away_points

        return total_points


    def get_total_win_since_beginning(self, team: str) -> int:

        list_of_years: list[int] = self.result_finder.get_list_of_years()

        total_wins_over_all_years: int = 0

        for year in list_of_years:

            total_wins: int = self.get_total_wins(year, team)

            total_wins_over_all_years += total_wins

        return total_wins_over_all_years


    def get_dictionary_of_wins(self, year: int) -> dict:

        list_of_teams: list[str] = self.get_list_of_teams(year)

        win_count_dictionary: dict[str:str] = {}
    
        for team in list_of_teams:

            total_wins: int = self.get_total_wins(year, team)

            win_count_dictionary[team] = total_wins

        return dict(sorted(win_count_dictionary.items()))

    
    def get_all_dictionary_of_wins(self) -> list:

        list_of_years: list[int] = self.result_finder.get_list_of_years()

        dictionary_of_year_to_leaderboard: dict = {} 
        list_of_dictionaries: list[dict[str:int]] = []

        for year in list_of_years:

            dictionary_of_wins: dict[str:int] = self.get_dictionary_of_wins(year)

            dictionary_of_year_to_leaderboard[year] = dictionary_of_wins

            list_of_dictionaries.append(dictionary_of_year_to_leaderboard)

        return list_of_dictionaries

    
    def get_all_time_dictionary_of_wins(self) -> dict:

        list_of_teams: list[str] = self.get_list_of_teams()

        win_count_dictionary: dict[str:str] = {}

        for team in list_of_teams:

            total_wins: int = self.get_total_win_since_beginning(team)

            win_count_dictionary[team] = total_wins

        return dict(sorted(win_count_dictionary.items()))


    def get_win_streaks(self, year: int, team: str) -> list:

        df = self.get_dataframe(year)

        new_df = df[(df["Home_Team"] == team) | (df["Away_Team"] == team)]

        list_of_streaks: list[int] = []
        streak: int = 0
        
        for i, record in new_df.iterrows():

            result: str = record["Result"]
            home_score = int(result[0])
            away_score = int(result[self.INDEX_OF_AWAY_TEAM])

            if (record["Home_Team"] == team) & (home_score > away_score):

                streak += 1

            elif (record["Away_Team"] == team) & (home_score < away_score):

                streak += 1

            else:

                list_of_streaks.append(streak)
                streak: int = 0

        return list_of_streaks

    
    def get_largest_win_streak(self, year: int, team: str) -> int:

        list_of_streaks: list[int] = self.get_win_streaks(year, team)

        return max(list_of_streaks)


    def get_largest_win_streak_for_all_teams(self, year: int) -> dict:
        
        list_of_teams: list[str] = self.get_list_of_teams(year)

        teams_with_streak: dict = {}

        for team in list_of_teams:

            win_streak = self.get_largest_win_streak(year, team)

            teams_with_streak[team] = win_streak

        return dict(sorted(teams_with_streak.items()))



if __name__ == "__main__":

    dataframe1 = DataframeAnalysis("premier_league")
    dataframe2 = DataframeAnalysis("championship")
    print(dataframe1.get_dictionary_of_wins(2000))
    print(dataframe1.get_all_time_dictionary_of_wins())
    # print(dataframe1.get_total_points(2000, "Arsenal"))