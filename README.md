# Football-Match-Outcome-Predictor

# Milestone 2

Milestone 2 introduces the beginning of analysing data through the perspective of a data scientist.Through observing the results provided, I have written a python class which could gather different types of information from the results.
Examples involve retrieving the number of wins per year from each league:

<img width="428" alt="image" src="https://user-images.githubusercontent.com/109103538/190437070-dec62cb6-528e-4d6d-9008-9db5e99f701d.png">

getting the winner of a match between two teams, given the league and year where the game took place.

<img width="570" alt="image" src="https://user-images.githubusercontent.com/109103538/190437540-5d8728f7-aa77-483d-8c0c-54d123af3f83.png">

getting the leaderboard of wins from each team in the form of a dictionary for each year.

<img width="525" alt="image" src="https://user-images.githubusercontent.com/109103538/190437764-1af5a496-5c3b-4963-90e4-8e1b61665320.png">

From my report, I have suggested some hypothesis regarding which statistics I think will be most important to consider when making the football predictor. One of which I think will have the biggest influence is the number of wins each team has from each year. The more recent the wins, the more weight they will likely have as their teams will still be similar with very few changes.


# Milestone 3

Milestone 3 required me to create methods which extracted data from the football csvs over all the years. For this, I created methods to gather the total wins, total goals and highest streak of every team throughout all the years. This was displayed in the form of a python dictionary where the team names were made to be the keys and the data were the values.

<img width="494" alt="image" src="https://user-images.githubusercontent.com/109103538/192159238-0ea05cc6-cd54-4c34-827f-77dc42b4265d.png">
<img width="484" alt="image" src="https://user-images.githubusercontent.com/109103538/192159268-c346313e-fbd5-48c6-83eb-a1f832deed38.png">
<img width="445" alt="image" src="https://user-images.githubusercontent.com/109103538/192159298-a6c0ef05-c1c3-4771-a4f1-30a29b13c241.png">

This data was then stored into a pandas dataframe which I made into a separate class.

<img width="569" alt="image" src="https://user-images.githubusercontent.com/109103538/192159387-5bc61ce3-7c47-4586-85dc-67b677a7a2b0.png">

Later, a method and class was made to store the dataframe as a csv file named "cleaned_dataset.csv". In the future, I can alter this method by making it take a path as an argument and this will make my method more general and allow the csv file to be stored into any path.

<img width="620" alt="image" src="https://user-images.githubusercontent.com/109103538/192159529-f1f81291-3bdb-4fd6-ac0e-cfda0542072a.png">

# Milestone 4

This milestone required me to spin up an RDS instance on aws. I made a postgres database as this is how I planned on upserting my data.

<img width="701" alt="image" src="https://user-images.githubusercontent.com/109103538/194354721-27f5dc22-11a8-4dc1-b4c7-725beb83ebe1.png">

Using psycopg2, I converted the pandas dataframe into a list form so that I could iterate over the list to upload each record to the postgres database. I first started by writing a method which would take sql code as an argument and this method would run the sql code in postgres.

<img width="659" alt="image" src="https://user-images.githubusercontent.com/109103538/194355768-dbab3627-0cfb-4f9b-923f-0cea3349a592.png">

I then wrote the method which would call the 'execute_to_postgres' method to make a table with the columns I list in the sql code.

<img width="501" alt="image" src="https://user-images.githubusercontent.com/109103538/194356229-baf87cb1-55a0-48e3-b9f9-f90ea733c984.png">

The 'get_all_records' method converts the pandas dataframe into a list of tuples where each tuple consista of the team, wins, streaks and goals.
I then iterated over the list and uploaded each tuple as a record to postgres.

<img width="512" alt="image" src="https://user-images.githubusercontent.com/109103538/194357285-00de1586-d007-452a-bac9-b2c97c4089da.png">

Final database on postgres:
<img width="311" alt="image" src="https://user-images.githubusercontent.com/109103538/194357958-5424cfc2-97a0-4b63-b6a6-99057a6e7b90.png">
