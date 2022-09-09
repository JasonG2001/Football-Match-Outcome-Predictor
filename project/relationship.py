import os

class ResultFinder:

    def go_to_football_league(self, football_league: str) -> None:

        try:

            os.chdir(fr"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results/{football_league}")

        except FileNotFoundError:

            print("This football league results cannot be found, please check the spelling.")

    def get_results(self, football_league: str, year: int) -> str:

        self.go_to_football_league(football_league)

        list_of_results: list[str] = os.listdir(fr"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results/{football_league}")
        index_of_thousands: int = 8
        index_of_ones: int = 12

        for annual_result in list_of_results:

            if str(year) == annual_result[index_of_thousands:index_of_ones]:
                
                return annual_result


if __name__ == "__main__":

    PATH = r"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results"
    result_finder = ResultFinder()
    result_finder.get_results("ligue_2", 2000)


