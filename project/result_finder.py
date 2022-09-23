import os

class ResultFinder:

    def __init__(self, football_league: str):

        self.football_league: str = football_league
        self.INDEX_OF_THOUSANDS: int = 8
        self.INDEX_OF_ONES: int = 12

    def go_to_football_league(self) -> None:

        try:

            os.chdir(fr"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results/{self.football_league}")

        except FileNotFoundError:

            print("This football league results cannot be found, please check the spelling.")

    def get_results(self, year: int) -> str:

        self.go_to_football_league()

        results: list[str] = os.listdir(fr"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results/{self.football_league}")

        for result in results:

            if str(year) == result[self.INDEX_OF_THOUSANDS:self.INDEX_OF_ONES]:
                
                return result

            
    def get_list_of_years(self) -> list:
        
        self.go_to_football_league()

        results: list[str] = os.listdir(fr"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results/{self.football_league}")

        years: list[int] = []

        for result in results:

            year = int(result[self.INDEX_OF_THOUSANDS:self.INDEX_OF_ONES])

            years.append(year)

        return years





if __name__ == "__main__":

    result_finder = ResultFinder("premier_league")
    print(result_finder.get_list_of_years())


 