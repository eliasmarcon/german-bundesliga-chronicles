import pandas as pd
import os
import time
import requests

from utils import create_final_table, get_matchdays


if __name__ == "__main__":
    
    # Create the dataset folder
    base_folder = "./dataset_folder"
    os.makedirs(base_folder, exist_ok=True)
    
    # Create the subfolders
    subfolders = ["1_bundesliga", "2_bundesliga", "3_liga"]
    for subfolder in subfolders:
        os.makedirs(f"{base_folder}/{subfolder}", exist_ok=True)
        

    # Define the league type
    bundesliga_types = ["bl1", "bl2", "bl3"]

    for index, bundesliga_type in enumerate(bundesliga_types):
        
        if bundesliga_type == "bl1":
            league_type = "1. Bundesliga"

        elif bundesliga_type == "bl2":
            league_type = "2. Bundesliga"

        elif bundesliga_type == "bl3":
            league_type = "3. Liga"

        else:
            league_type = "Unknown"

        # Create the dataframes
        overall_dataframe = pd.DataFrame(columns=["League", "Season", "Matchday", "Match_Date", "Match_Time", "Home_Team", "Home_Team_Short", "Guest_Team", 
                                                  "Guest_Team_Short", "Home_Goals", "Guest_Goals", "Home_Points", "Guest_Points", 
                                                  "Location", "Stadium", "Viewers"])

        goals_df = pd.DataFrame(columns=["League", "Season", "Match_Day", "Team", "Player_Firstname", "Player_Surname",
                                         "Match_Minute", "Game_Score", "is_Penalty", "is_Own_Goal", "is_Overtime"])


        print(f"Starting to get data for {league_type}")

        # Get the data
        for season in range(2004, 2025): # 2004 - 2025

            for match_day in range(1, 39):
                
                if bundesliga_type != "bl3" and match_day > 34:
                    continue

                # Form the URL
                url = f"https://api.openligadb.de/getmatchdata/{bundesliga_type}/{season}/{match_day}"
                
                try:

                    response = requests.get(url)

                    # Check if the response status is OK
                    if response.status_code != 200:
                        print(f"Error retrieving data for {season}, Matchday {match_day}")
                        continue  # Skip to the next match day

                    else:
                        # Process the response
                        json_responses = response.json()
                        
                        # Get the matchdays
                        overall_dataframe, goals_df = get_matchdays(json_responses, league_type, overall_dataframe, goals_df)
                        
                except requests.exceptions.RequestException as e:
                        print(f"Request failed for {season}, Matchday {match_day}: {e}")
                        continue
                
            print(f"|---- Season {season}/{season + 1} done")
            
            # Wait for 5 seconds to not get blocked by the API
            time.sleep(5)
            
        # Create the past seasons dataset
        overall_dataframe.to_csv(f"{base_folder}/{subfolders[index]}/{subfolders[index]}_overall.csv", index=False, encoding="utf-8-sig")
        goals_df.to_csv(f"{base_folder}/{subfolders[index]}/{subfolders[index]}_goal_scorers.csv", index=False, encoding="utf-8-sig")
        
        # Create the final table
        seasonal_final_table_df = create_final_table(overall_dataframe)
        seasonal_final_table_df.to_csv(f"{base_folder}/{subfolders[index]}/{subfolders[index]}_final_table.csv", index=False, encoding="utf-8-sig")
            
        print(f"League {league_type} done\n")