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

    def get_teams(self, year: int = None) -> set:

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


    def get_teams_indexed(self) -> dict:

        teams: set[str] = self.get_teams()

        sorted_teams: list[str] = sorted(list(teams))

        teams_indexed: dict[int:str] = {}
        
        team: str
        for team in sorted_teams:

            teams_indexed[sorted_teams.index(team)] = team  

        return teams_indexed

    
    def get_number_of_teams(self, year: int = None) -> str:

        teams: list[str] = self.get_teams(year)

        try:
            
            return len(teams)

        except:

            print("No record for this league")


    def get_winner(self, year: int, home_team: str, away_team: str) -> str:

        df = self.get_dataframe(year) # returns df

        new_df = df[(df["Home_Team"] == home_team) & (df["Away_Team"] == away_team)]

        result = new_df.loc[:, "Result"]

        for i, score in enumerate(result):
            
            home_score = int(score[0])
            away_score = int(score[self.INDEX_OF_AWAY_TEAM])

            if home_score > away_score:

                return home_team

            elif home_score < away_score:

                return away_team

            else:

                return "draw"

    
    def get_home_wins(self, year: int, team: str) -> int:

        df = self.get_dataframe(year)

        new_df = df[df["Home_Team"] == team]

        home_wins: int = 0

        result = new_df.loc[:, "Result"]

        for i, score in enumerate(result):

            home_score = int(score[0])
            away_score = int(score[self.INDEX_OF_AWAY_TEAM])

            if home_score > away_score:

                home_wins += 1

        return home_wins

    
    def get_away_wins(self, year: int, team: str) -> int:

        df = self.get_dataframe(year)

        new_df = df[df["Away_Team"] == team]

        away_wins: int = 0

        result = new_df.loc[:, "Result"]

        for i, score in enumerate(result):

            home_score = int(score[0])
            away_score = int(score[self.INDEX_OF_AWAY_TEAM])

            if home_score < away_score:

                away_wins += 1

        return away_wins


    def get_total_wins(self, year: int, team: str) -> int:

        home_wins: int = self.get_home_wins(year, team)
        away_wins: int = self.get_away_wins(year, team)

        total_wins: int = home_wins + away_wins

        return total_wins


    def get_home_goals(self, year: int, team: str) -> int:

        df = self.get_dataframe(year)

        new_df = df[df["Home_Team"] == team]

        home_goals: int = 0

        result = new_df.loc[:, "Result"]
        
        score: str       
        for _, score in enumerate(result):

            goals = int(score[0])

            home_goals += goals

        return home_goals


    def get_away_goals(self, year: int, team: str) -> int:

        df = self.get_dataframe(year)

        new_df = df[df["Away_Team"] == team]

        away_goals: int = 0

        result = new_df.loc[:, "Result"]

        for i, score in enumerate(result):

            goals = int(score[self.INDEX_OF_AWAY_TEAM])

            away_goals += goals

        return away_goals


    def get_total_goals(self, year: int, team: str) -> int:

        home_points: int = self.get_home_goals(year, team)
        away_points: int = self.get_away_goals(year, team)

        total_goals: int = home_points + away_points

        return total_goals


    def get_total_goals_over_all_years(self, team: str) -> int:

        years: list[int] = self.result_finder.get_list_of_years()

        total_goals_over_all_years: int = 0

        for year in years:

            total_goals = self.get_total_goals(year, team)

            total_goals_over_all_years += total_goals

        return total_goals_over_all_years


    def get_goal_board_over_all_years(self) -> dict:

        goal_board_over_all_years: dict[str:int] = {}

        teams: list[str] = self.get_teams()

        for team in teams:

            total_goals_over_all_years: int = self.get_total_goals_over_all_years(team)

            goal_board_over_all_years[team] = total_goals_over_all_years

        return dict(sorted(goal_board_over_all_years.items()))


    def get_total_wins_over_all_years(self, team: str) -> int:

        years: list[int] = self.result_finder.get_list_of_years()

        total_wins_over_all_years: int = 0

        for year in years:

            total_wins: int = self.get_total_wins(year, team)

            total_wins_over_all_years += total_wins

        return total_wins_over_all_years


    def get_win_board(self, year: int) -> dict:

        teams: list[str] = self.get_teams(year)

        win_board: dict[str:str] = {}
    
        for team in teams:

            total_wins: int = self.get_total_wins(year, team)

            win_board[team] = total_wins

        return dict(sorted(win_board.items()))

    
    def get_all_win_boards(self) -> list:

        years: list[int] = self.result_finder.get_list_of_years()

        win_board_for_each_year: dict = {} 
        all_win_boards: list[dict[str:int]] = []

        for year in years:

            win_board: dict[str:int] = self.get_win_board(year)

            win_board_for_each_year[year] = win_board

            all_win_boards.append(win_board_for_each_year)

        return all_win_boards

    
    def get_win_board_over_all_years(self) -> dict:

        teams: list[str] = self.get_teams()

        win_board_over_all_years: dict[str:str] = {}

        for team in teams:

            total_wins_over_all_years: int = self.get_total_wins_over_all_years(team)

            win_board_over_all_years[team] = total_wins_over_all_years

        return dict(sorted(win_board_over_all_years.items()))


    def get_largest_streak(self, year: int, team: str) -> list:

        df = self.get_dataframe(year)

        new_df = df[(df["Home_Team"] == team) | (df["Away_Team"] == team)]

        streaks: list[int] = []
        streak: int = 0
        
        for _, record in new_df.iterrows():

            result: str = record["Result"]
            home_score = int(result[0])
            away_score = int(result[self.INDEX_OF_AWAY_TEAM])

            if (record["Home_Team"] == team) & (home_score > away_score):

                streak += 1

            elif (record["Away_Team"] == team) & (home_score < away_score):

                streak += 1

            else:

                streaks.append(streak)
                streak: int = 0

        return max(streaks, default=0) # Needs fixing as a team that wins all games will never have streak appended


    def get_largest_streak_over_all_years(self, team: str) -> int:

        years: list[int] = self.result_finder.get_list_of_years()

        streaks: list[int] = []

        for year in years:

            streak: int = self.get_largest_streak(year, team)

            streaks.append(streak)

        return max(streaks)


    def get_largest_streak_board_over_all_years(self):

        teams: list[str] = self.get_teams()

        streak_board_over_all_years: dict[str:int] = {}

        for team in teams:

            largest_streak: int = self.get_largest_streak_over_all_years(team)

            streak_board_over_all_years[team] = largest_streak

        return dict(sorted(streak_board_over_all_years.items()))


    def get_largest_streak_board_for_all_teams(self, year: int) -> dict:
        
        teams: list[str] = self.get_teams(year)

        streak_board: dict = {}

        for team in teams:

            win_streak = self.get_largest_streak(year, team)

            streak_board[team] = win_streak

        return dict(sorted(streak_board.items()))



if __name__ == "__main__":

    dataframe1 = DataframeAnalysis("premier_league")
    dataframe2 = DataframeAnalysis("championship")
    # print(dataframe1.get_largest_streak_over_all_years("Arsenal"))
    #print(dataframe1.get_teams())
    print(dataframe1.get_goal_board_over_all_years())
    # print(dataframe1.get_total_points(2000, "Arsenal"))
    print(dataframe1.get_elo())
    # print(dataframe1.get_largest_streak_board_over_all_years())