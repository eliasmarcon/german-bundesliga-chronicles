import pandas as pd


def scored_goals(league_type, season, matchday, goals, team1, team2):

    sorted_goals = sorted(
        [g for g in goals if g["matchMinute"] is not None], 
        key=lambda x: x["matchMinute"]
    )
        
    # Original score before this goal was scored (assumed 0:0)
    original_score_team1 = 0
    original_score_team2 = 0

    df_row = {"League" : [], "Season" : [], "Match_Day" : [], "Team" : [], "Player_Firstname" : [], "Player_Surname" : [],
              "Match_Minute" : [], "Game_Score" : [], "is_Penalty" : [], "is_Own_Goal" : [], "is_Overtime" : []}

    for goal in sorted_goals:

        team_scored = None

        if goal["matchMinute"] is not None and goal["goalGetterName"]:

            # Add the goal to the teams
            if isinstance(goal["scoreTeam1"], int) and goal["scoreTeam1"] > original_score_team1:
                original_score_team1 += 1
                team_scored = team1

            elif isinstance(goal["scoreTeam2"], int) and goal["scoreTeam2"] > original_score_team2:
                original_score_team2 += 1
                team_scored = team2

            # If a goal was scored, add it to the dataframe
            if team_scored:

                # Add the goal to the dataframe
                df_row["League"].append(league_type)
                df_row["Season"].append(season)
                df_row["Match_Day"].append(matchday)
                df_row["Team"].append(team_scored)
                df_row["Player_Firstname"].append(goal["goalGetterName"].split(" ")[0] if len(goal["goalGetterName"].split(" ")) > 1 else "")
                df_row["Player_Surname"].append(goal["goalGetterName"].split(" ")[1] if len(goal["goalGetterName"].split(" ")) > 1 else goal["goalGetterName"])
                df_row["Match_Minute"].append(goal["matchMinute"])
                df_row["Game_Score"].append(f"{original_score_team1}:{original_score_team2}")
                df_row["is_Penalty"].append(False if goal["isPenalty"] in [False, 0] else True)
                df_row["is_Own_Goal"].append(False if goal["isOwnGoal"] in [False, 0] else True)
                df_row["is_Overtime"].append(False if goal["isOvertime"] in [False, 0] else True)

    return pd.DataFrame(df_row)


def get_matchdays(json_responses, league_type, overall_dataframe, goals_df):

    for json_response in json_responses:

        if json_response.get("matchIsFinished"):

            full_season = f"{json_response['leagueSeason']}/{json_response['leagueSeason'] + 1}"
            
            if json_response.get("matchDateTime"):
                match_date_time = json_response.get("matchDateTime")
                match_date = match_date_time.split("T")[0]
                match_time = match_date_time.split("T")[1]
                
            else:
                match_date = "Unknown"
                match_time = "Unknown"

            matchday = json_response["group"]["groupName"]

            # Continue if mathday has not a number in it
            if not any(char.isdigit() for char in matchday):
                continue
            
            team1 = json_response["team1"]["teamName"]
            team1_shortname = json_response["team1"]["shortName"]

            if team1_shortname == "" and team1 == "TSG 1899 Hoffenheim":
                team1_shortname = "TSG"

            team2 = json_response["team2"]["teamName"]
            team2_shortname = json_response["team2"]["shortName"]

            if team2_shortname == "" and team2 == "TSG 1899 Hoffenheim":
                team2_shortname = "TSG"

            # Get the goals scored by each team
            endergebnis = next((result for result in json_response["matchResults"] if result["resultName"] == "Endergebnis"), None)
            goals_team1 = endergebnis["pointsTeam1"] if endergebnis else 0
            goals_team2 = endergebnis["pointsTeam2"] if endergebnis else 0

            # Get the points for each team
            points_team1 = 3 if goals_team1 > goals_team2 else 1 if goals_team1 == goals_team2 else 0
            points_team2 = 3 if goals_team1 < goals_team2 else 1 if goals_team1 == goals_team2 else 0

            # Get the location of the match
            if json_response.get("location") is None:
                location = "Unknown"
                location_stadium = "Unknown"
            
            else:
                location = json_response.get("location", {}).get("locationCity", "Unknown")
                location_stadium = json_response.get("location", {}).get("locationStadium", "Unknown") 
                
            # Get the number of viewers
            number_of_viewers = json_response.get("numberOfViewers", -1) or -1
            
            # Create a new dataframe
            new_dataframe = pd.DataFrame([[league_type, full_season, matchday, match_date, match_time, team1, team1_shortname, team2, 
                                           team2_shortname, goals_team1, goals_team2, points_team1, points_team2, location, 
                                           location_stadium, number_of_viewers]], columns=overall_dataframe.columns)
            
            if len(overall_dataframe) == 0:
                overall_dataframe = new_dataframe
            else:
                overall_dataframe = pd.concat([overall_dataframe, new_dataframe], ignore_index=True)

            if goals_team1 > 0 or goals_team2 > 0 and len(json_response["goals"]) > 0:
                
                scored_game_df = scored_goals(league_type, full_season, matchday, json_response["goals"], team1, team2)
                goals_df = pd.concat([goals_df, scored_game_df], ignore_index=True)
                
    return overall_dataframe, goals_df


def create_final_table(overall_dataframe):
    
    league_type = overall_dataframe["League"].iloc[0]
    
    # Creating home and guest stats
    home_stats = overall_dataframe.rename(columns={
        "Home_Team": "Team", "Home_Team_Short": "Team_Short", 
        "Home_Goals": "Goals", "Guest_Goals": "Opponent_Goals", 
        "Home_Points": "Points"
    }).assign(
        Matches=1, Won=(overall_dataframe["Home_Points"] == 3).astype(int), 
        Draw=(overall_dataframe["Home_Points"] == 1).astype(int), 
        Lost=(overall_dataframe["Home_Points"] == 0).astype(int)
    ).loc[:, ["Season", "Team", "Team_Short", "Matches", "Points", "Won", "Lost", "Draw", "Goals", "Opponent_Goals"]]


    guest_stats = overall_dataframe.rename(columns={
        "Guest_Team": "Team", "Guest_Team_Short": "Team_Short", 
        "Guest_Goals": "Goals", "Home_Goals": "Opponent_Goals", 
        "Guest_Points": "Points"
    }).assign(
        Matches=1, Won=(overall_dataframe["Guest_Points"] == 3).astype(int), 
        Draw=(overall_dataframe["Guest_Points"] == 1).astype(int), 
        Lost=(overall_dataframe["Guest_Points"] == 0).astype(int)
    ).loc[:, ["Season", "Team", "Team_Short", "Matches", "Points", "Won", "Lost", "Draw", "Goals", "Opponent_Goals"]]

    # Combine home and guest stats
    seasonal_final_table_df = pd.concat([home_stats, guest_stats])

    # Group by season and team, then sum up stats
    seasonal_final_table_df = seasonal_final_table_df.groupby(["Season", "Team", "Team_Short"], as_index=False).sum()

    # Calculate Goal Difference
    seasonal_final_table_df["GoalDiff"] = seasonal_final_table_df["Goals"] - seasonal_final_table_df["Opponent_Goals"]

    # Sort by season and points
    seasonal_final_table_df = seasonal_final_table_df.sort_values(["Season", "Points", "GoalDiff", "Goals"], ascending=[True, False, False, False])
    
    # Append the league on first position
    seasonal_final_table_df.insert(0, "League", league_type)
    
    return seasonal_final_table_df