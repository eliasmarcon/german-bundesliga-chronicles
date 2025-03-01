# German Bundesliga Chronicles


This dataset provides comprehensive details about football matches, goal scorers, and final standings from various leagues, offering rich insights into football performance.

- Overall Match Dataset: Includes match details such as matchday, teams, scores, and timing for every match, allowing for analysis of team performance, match trends, and more.
- Goal Scorer Dataset: Focuses on goal-related information, including players, timing, and whether the goal was a penalty, own goal, or in overtime, ideal for identifying key contributors and goal trends.
- Final Table Dataset: Contains league standings, summarizing team performance with metrics like wins, losses, goals scored, and points, useful for season-over-season comparisons and trend analysis.


The original data can be found at [OpenLigaDB](https://www.openligadb.de/), and there's also an [API here](https://api.openligadb.de/index.html). Additionally, the full dataset is available on [Kaggle](https://www.kaggle.com/datasets/eliasmarcon/german-bundesliga-chronicles).


### **Please note that the data may not be 100% accurate, as it's a free API and the games are maintained by the community.**


The folder structure of the project is the following:

```
📦 github
 ┣ 📂 workflows
 ┃ ┗ 📄 kaggle_upload.yaml                # GitHub Actions workflow for automatic dataset upload to Kaggle
 ┣ 📂 dataset_folder
 ┃ ┣ 📂 1_bundesliga
 ┃ ┃ ┣ 📄 1_bundesliga_final_table.csv    # Season-end standings with points, wins, losses, etc.
 ┃ ┃ ┣ 📄 1_bundesliga_goal_scorers.csv   # Top goal scorers with player statistics
 ┃ ┃ ┗ 📄 1_bundesliga_overall.csv        # Comprehensive match data for the season
 ┃ ┣ 📂 2_bundesliga
 ┃ ┃ ┣ 📄 2_bundesliga_final_table.csv    # Season-end standings for 2. Bundesliga
 ┃ ┃ ┣ 📄 2_bundesliga_goal_scorers.csv   # Goal scorer statistics for 2. Bundesliga
 ┃ ┃ ┗ 📄 2_bundesliga_overall.csv        # Complete match data for 2. Bundesliga
 ┃ ┣ 📂 3_liga
 ┃ ┃ ┣ 📄 3_liga_final_table.csv          # Season-end standings for 3. Liga
 ┃ ┃ ┣ 📄 3_liga_goal_scorers.csv         # Goal scorer statistics for 3. Liga
 ┃ ┃ ┗ 📄 3_liga_overall.csv              # Complete match data for 3. Liga
 ┃ ┗ 📄 dataset-metadata.json             # Metadata describing the dataset for Kaggle
 ┣ 📂 src
 ┃ ┣ 📄 generate_past_seasons_dataset.py  # Script to generate historical season data
 ┃ ┣ 📄 update_past_seasons_dataset.py    # Script to update dataset with latest results
 ┃ ┣ 📄 utils.py                          # Utility functions used by the other scripts
 ┣ 📄 .gitignore                          # Specifies files/directories to be ignored by Git
 ┣ 📄 LICENSE                             # License information for the project
 ┗ 📄 README.md                           # Project documentation and usage instructions
```

To run the Python scripts `generate_past_seasons_dataset.py` and `update_past_seasons_dataset.py`, execute them from the main project folder (do not navigate into the `src` directory).  

Use the following commands:  
```
python ./src/generate_past_seasons_dataset.py  
python ./src/update_past_seasons_dataset.py  
```


<br>
<hr style="border: 3px solid gray;">
<br>

# Overall Match Dataset (`**league**_overall.csv`)

This dataset contains details about football matches, including match timing, teams, score, and other related information.

## Columns Explanation

| Column            | Description |
|------------------|-------------|
| **League**       | Name of the football league (e.g., "1. Bundesliga"). |
| **Season**       | The season in `YYYY/YYYY` format (e.g., "2004/2005"). |
| **Matchday**     | The matchday or round number in the season (e.g., "1. Spieltag" for the first matchday). |
| **Match_Date**   | The date the match was played in `YYYY-MM-DD` format (e.g., "2004-08-06"). |
| **Match_Time**   | The time the match started in `HH:MM:SS` format (e.g., "21:35:00"). |
| **Home_Team**    | The name of the home team (e.g., "Werder Bremen"). |
| **Home_Team_Short** | The short name for the home team (e.g., "Bremen"). |
| **Guest_Team**   | The name of the guest team (e.g., "FC Schalke 04"). |
| **Guest_Team_Short** | The short name for the guest team (e.g., "Schalke"). |
| **Home_Goals**   | The number of goals scored by the home team in the match (e.g., 1). |
| **Guest_Goals**  | The number of goals scored by the guest team in the match (e.g., 0). |
| **Home_Points**  | The points awarded to the home team (typically **3** for a win, **0** for a loss, or **1** for a draw). |
| **Guest_Points** | The points awarded to the guest team (same logic as `Home_Points`). |
| **Location**     | The location of the match (e.g., "Unknown" if not specified). |
| **Stadium**      | The stadium where the match was played (e.g., "Unknown" if not specified). |
| **Viewers**      | The number of viewers (e.g., "-1" if not available or unspecified). |

## Example Data Entry

| League        | Season   | Matchday     | Match_Date | Match_Time | Home_Team      | Home_Team_Short | Guest_Team    | Guest_Team_Short | Home_Goals | Guest_Goals | Home_Points | Guest_Points | Location | Stadium | Viewers |
|--------------|----------|--------------|------------|------------|----------------|-----------------|---------------|------------------|------------|-------------|-------------|--------------|----------|---------|---------|
| 1. Bundesliga | 2004/2005 | 1. Spieltag | 2004-08-06 | 21:35:00   | Werder Bremen  | Bremen          | FC Schalke 04 | Schalke          | 1          | 0           | 3           | 0            | Unknown  | Unknown | -1      |

## Usage
This dataset is useful for:
- Analyzing match results including goals, points, and teams.
- Studying match timings and viewer data (if available).
- Understanding team performances based on match outcomes.

<br>
<hr style="border: 3px solid gray;">
<br>

# Goal Scorer Dataset (`**league**_goal_scorer.csv`)

This dataset contains information about goals scored in football matches, including details about the player, match timing, and goal type.

## Columns Explanation

| Column          | Description |
|----------------|-------------|
| **League**     | Name of the football league (e.g., "1. Bundesliga"). |
| **Season**     | The season in `YYYY` format (e.g., "2009"). |
| **Match_Day**  | The matchday or round number in the season (e.g., "1. Spieltag" for the first matchday). |
| **Team**       | Name of the team that scored the goal. |
| **Player_Name** | Name of the player who scored the goal. |
| **Match_Minute** | The minute in which the goal was scored (e.g., "71.0" for the 71st minute). |
| **Match_Stand** | The scoreline at the time of the goal (e.g., "1:0" means the scoring team was leading 1-0). |
| **is_Penalty**  | Indicates if the goal was scored from a penalty (**1 = Yes, 0 = No**). |
| **is_Own_Goal** | Indicates if it was an own goal (**1 = Yes, 0 = No**). |
| **is_Overtime** | Indicates if the goal was scored in overtime/extra time (**1 = Yes, 0 = No**). |

## Example Data Entry

| League        | Season | Match_Day   | Team           | Player_Name | Match_Minute | Match_Stand | is_Penalty | is_Own_Goal | is_Overtime |
|--------------|--------|------------|---------------|-------------|--------------|-------------|------------|-------------|-------------|
| 1. Bundesliga | 2009   | 1. Spieltag | VfL Wolfsburg | Misimovic   | 71.0         | 1:0         | 0          | 0           | 0           |

## Usage
This dataset is useful for:
- Analyzing goal-scoring trends in different leagues and seasons.
- Identifying top goal scorers and their impact on match results.
- Studying the frequency of penalties, own goals, and overtime goals.

<br>
<hr style="border: 3px solid gray;">
<br>

# Final Table Dataset (`**league**_final_table.csv`)

This dataset contains football league standings, including team performance metrics for each season.

## Columns Explanation

| Column            | Description |
|------------------|-------------|
| **League**       | Name of the football league (e.g., "1. Bundesliga"). |
| **Season**       | The season in `YYYY/YYYY` format (e.g., "2004/2005"). |
| **Team**         | Full name of the football team (e.g., "FC Bayern München"). |
| **Team_Short**   | Shortened version of the team name (e.g., "Bayern"). |
| **Matches**      | Total number of matches played in that season. |
| **Points**       | Total points accumulated (3 for a win, 1 for a draw, 0 for a loss). |
| **Won**          | Number of matches won by the team. |
| **Lost**         | Number of matches lost by the team. |
| **Draw**         | Number of matches that ended in a draw. |
| **Goals**        | Total goals scored by the team in the season. |
| **Opponent_Goals** | Total goals conceded by the team. |
| **GoalDiff**     | Goal difference (`Goals - Opponent_Goals`). A positive value means more goals scored than conceded. |

## Example Data Entry

| League        | Season   | Team                | Team_Short | Matches | Points | Won | Lost | Draw | Goals | Opponent_Goals | GoalDiff |
|--------------|---------|---------------------|------------|---------|--------|-----|------|------|-------|----------------|----------|
| 1. Bundesliga | 2004/2005 | FC Bayern München | Bayern     | 34      | 77     | 24  | 5    | 5    | 75    | 33             | 42       |

## Usage
This dataset is useful for:
- Analyzing team performance across seasons.
- Identifying trends in wins, goals, and points.
- Predicting future league standings based on past data.