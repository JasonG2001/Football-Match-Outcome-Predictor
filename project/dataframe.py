from result_finder import ResultFinder
from typing import Dict, List, Set, Type
import pandas as pd
import pickle

class DataframeAnalysis:

    def __init__(self) -> None:

        self.result_finder = ResultFinder()
        self.INDEX_OF_HOME_TEAM_SCORE: int = 0
        self.INDEX_OF_AWAY_TEAM_SCORE: int = 2


    def get_dataframe(self, football_league: str, year: int) -> Type[pd.DataFrame]:
        
        result: str = self.result_finder.get_results(football_league, year)
            
        df: Type[pd.Dataframe] = pd.read_csv(fr"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results/{football_league}/{result}")

        return df


    def get_elo(self) -> Dict[str,Dict[str,float]]:

        elo: Dict[str,Dict[str,float]] = pickle.load(open('/home/jason2001/Football-Match-Outcome-Predictor/project/elo_dict.pkl', 'rb'))

        return elo


    def get_team_template(self, football_league: str, year: int) -> Dict[str,int]:

        home_teams: Type[pd.DataFrame] = self.get_dataframe(football_league, year)["Home_Team"]
        away_teams: Type[pd.DataFrame] = self.get_dataframe(football_league, year)["Away_Team"]

        teams: Set(str) = set(home_teams)
        
        teams.update(set(away_teams))

        return {team:0 for team in teams}


    def get_home_and_away_elos(self, football_league: str, year: int) -> List[float]:

        links: Type[pd.DataFrame] = self.get_dataframe(football_league, year).loc[:, "Link"]
        elo: Dict[str,Dict[str,float]] = self.get_elo()
        home_elos: List[float] = []
        away_elos: List[float] = []

        link: str
        for _, link in enumerate(links):

            home_elos.append(elo[link]["Elo_home"])
            away_elos.append(elo[link]["Elo_away"])
            
        return home_elos, away_elos


    def get_home_and_away_goals_so_far(self, football_league: str, year: int) -> List[int]:

        team_template: Dict[str,int] = self.get_team_template(football_league, year)

        df: Type[pd.DataFrame] = self.get_dataframe(football_league, year).loc[:, ["Home_Team", "Away_Team", "Result"]]
        
        home_goals_so_far: List[int] = []
        away_goals_so_far: List[int] = []

        for _, record in df.iterrows():

            home_team: str = record.loc["Home_Team"]
            away_team: str = record.loc["Away_Team"]

            home_goals_so_far.append(team_template[home_team]) 
            away_goals_so_far.append(team_template[away_team])

            home_team_score: int = int(record.loc["Result"][self.INDEX_OF_HOME_TEAM_SCORE])
            away_team_score: int = int(record.loc["Result"][self.INDEX_OF_AWAY_TEAM_SCORE])

            team_template[home_team] += home_team_score
            team_template[away_team] += away_team_score

        return home_goals_so_far, away_goals_so_far
    

    def get_wins_losses_draws_so_far(self, football_league: str, year: int) -> List[int]:

        team_wins_template: Dict[str,int] = self.get_team_template(football_league, year)
        team_losses_template: Dict[str,int] = self.get_team_template(football_league, year)
        team_draws_template: Dict[str,int] = self.get_team_template(football_league, year)

        df: Type[pd.DataFrame] = self.get_dataframe(football_league, year). \
        loc[:, ["Home_Team", "Away_Team", "Result"]]
        
        home_wins_so_far: List[int] = []
        away_wins_so_far: List[int] = []
        home_losses_so_far: List[int] = []
        away_losses_so_far: List[int] = []
        home_draws_so_far: List[int] = []
        away_draws_so_far: List[int] = []

        for _, record in df.iterrows():

            home_team: str = record.loc["Home_Team"]
            away_team: str = record.loc["Away_Team"]

            home_wins_so_far.append(team_wins_template[home_team])
            away_wins_so_far.append(team_wins_template[away_team])
            home_losses_so_far.append(team_losses_template[home_team])
            away_losses_so_far.append(team_losses_template[away_team])
            home_draws_so_far.append(team_draws_template[home_team])
            away_draws_so_far.append(team_draws_template[away_team])

            home_team_score: int = int(record.loc["Result"][self.INDEX_OF_HOME_TEAM_SCORE])
            away_team_score: int = int(record.loc["Result"][self.INDEX_OF_AWAY_TEAM_SCORE])

            if home_team_score > away_team_score:
                team_wins_template[home_team] += 1
                team_losses_template[away_team] += 1

            elif home_team_score < away_team_score:
                team_wins_template[away_team] += 1
                team_losses_template[home_team] += 1

            else:
                team_draws_template[home_team] += 1
                team_draws_template[away_team] += 1

        return home_wins_so_far, away_wins_so_far, home_losses_so_far, away_losses_so_far, home_draws_so_far, away_draws_so_far


    def get_current_streak(self, football_league: str, year: int) -> List[int]:

        team_streaks_template: Dict[str:int] = self.get_team_template(football_league, year)

        df: Type[pd.DataFrame] = self.get_dataframe(football_league, year). \
        loc[:, ["Home_Team", "Away_Team", "Result"]]

        current_home_streak: List[int] = []
        current_away_streak: List[int] = []

        for _, record in df.iterrows():

            home_team: str = record.loc["Home_Team"]
            away_team: str = record.loc["Away_Team"]

            current_home_streak.append(team_streaks_template[home_team])
            current_away_streak.append(team_streaks_template[away_team])

            home_team_score: int = int(record.loc["Result"][self.INDEX_OF_HOME_TEAM_SCORE])
            away_team_score: int = int(record.loc["Result"][self.INDEX_OF_AWAY_TEAM_SCORE])

            if home_team_score > away_team_score:
                team_streaks_template[home_team] += 1
                team_streaks_template[away_team] = 0

            elif home_team_score < away_team_score:
                team_streaks_template[home_team] = 0
                team_streaks_template[away_team] += 1

            else:
                team_streaks_template[home_team] = 0
                team_streaks_template[away_team] = 0

        return current_home_streak, current_away_streak

        
    def get_result(self, football_league: str, year: int) -> List[int]:

        df: Type[pd.DataFrame] = self.get_dataframe(football_league, year).loc[:, ["Result"]]

        home_results: List[str] = []
        away_results: List[str] = []

        for _, result in df.iterrows():

            home_score: int = int(result.loc["Result"][self.INDEX_OF_HOME_TEAM_SCORE])
            away_score: int = int(result.loc["Result"][self.INDEX_OF_AWAY_TEAM_SCORE])

            if home_score > away_score:
                home_results.append("win")
                away_results.append("lose")

            elif home_score < away_score:
                home_results.append("lose")
                away_results.append("win")

            else:
                home_results.append("draw")
                away_results.append("draw")

        return home_results, away_results


if __name__ == "__main__":

    dataframe = DataframeAnalysis()
    print(dataframe.get_home_and_away_elos("premier_league", 2021))
    print(dataframe.get_home_and_away_goals_so_far("premier_league", 2021))
    print(dataframe.get_wins_losses_draws_so_far("premier_league", 2021))
    print(dataframe.get_current_streak("premier_league", 2021))
    print(dataframe.get_result("premier_league", 2021))