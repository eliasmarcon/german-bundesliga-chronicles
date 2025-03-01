import pandas as pd
import requests

from utils import create_final_table, get_matchdays


if __name__ == "__main__":
    
    # Load the dataset
    base_folder = "./dataset_folder"

    # Define the league type
    subfolders = ["1_bundesliga", "2_bundesliga", "3_liga"]
    bundesliga_types = ["bl1", "bl2", "bl3"]

    for index, bundesliga_type in enumerate(bundesliga_types):

        overall_dataframe = pd.read_csv(f"{base_folder}/{subfolders[index]}/{subfolders[index]}_overall.csv")
        goals_df = pd.read_csv(f"{base_folder}/{subfolders[index]}/{subfolders[index]}_goal_scorers.csv")
        
        # Get the league type
        league_type = overall_dataframe["League"].iloc[0]
        
        # Get the latest season
        latest_season = overall_dataframe["Season"].str.split("/").apply(lambda x: int(x[0])).max()

        # Get the latest mathday
        latest_matchday = overall_dataframe[overall_dataframe["Season"] == f"{latest_season}/{latest_season+1}"]["Matchday"].str.split(".").apply(lambda x: int(x[0])).max()

        if latest_matchday == 34 and bundesliga_type != "bl3":
            latest_season += 1
            latest_matchday = 0
            
        elif latest_matchday == 38 and bundesliga_type == "bl3":
            latest_season += 1
            latest_matchday = 0
            
        # Get the new matchday
        new_matchday = latest_matchday + 1
        
        # Form the URL
        url = f"https://api.openligadb.de/getmatchdata/{bundesliga_type}/{latest_season}/{new_matchday}"

        try:

            response = requests.get(url)
            
            # Check if the response status is OK
            if response.status_code != 200:
                print(f"Error retrieving data for {latest_season}, Matchday {new_matchday}")
                
            elif not response.json()[0].get("matchIsFinished"):
                print(f"Matchday {new_matchday} for {subfolders[index]} and Season {latest_season} has not been played yet.")
                
            else:
        
                # Process the response
                json_responses = response.json()
                
                # Get the matchdays
                overall_dataframe, goals_df = get_matchdays(json_responses, league_type, overall_dataframe, goals_df)
                
                # Create the past seasons dataset
                overall_dataframe.to_csv(f"{base_folder}/{subfolders[index]}/{subfolders[index]}_overall.csv", index=False, encoding="utf-8-sig")
                goals_df.to_csv(f"{base_folder}/{subfolders[index]}/{subfolders[index]}_goal_scorers.csv", index=False, encoding="utf-8-sig")
                
                # Create the final table
                seasonal_final_table_df = create_final_table(overall_dataframe)
                seasonal_final_table_df.to_csv(f"{base_folder}/{subfolders[index]}/{subfolders[index]}_final_table.csv", index=False, encoding="utf-8-sig")
                
                print(f"Data for {subfolders[index]}, Season {latest_season}, Matchday {new_matchday} has been retrieved successfully.")
            
        except Exception as e:
            print(f"Something went wrong. {e}")