import random
import tkinter as tk
from tkinter import ttk

# Define a Team class to represent a football team
class Team:
    def __init__(self, name, rating):
        self.name = name
        self.rating = float(rating)
        self.points = 0
        self.goals_scored = 0
        self.goals_conceded = 0

# Define a Match class to represent a football match
class Match:
    def __init__(self, team1, team2, winner):
        self.team1 = team1
        self.team2 = team2
        self.winner = winner

# Define a function to simulate a match between two teams
def simulate_match(team1, team2):
    rating_diff = team1.rating - team2.rating
    win_probability = 1 / (1 + 10 ** (-rating_diff / 400))  # Calculate win probability using Elo rating formula
    result = random.choices([team1, team2, None], weights=[win_probability, 1 - win_probability, 0], k=1)[0]

    if result == team1:
        team1.points += 3
        team1.goals_scored += 1
        team2.goals_conceded += 1
    elif result == team2:
        team2.points += 3
        team2.goals_scored += 1
        team1.goals_conceded += 1
    else:
        team1.points += 1
        team2.points += 1
        team1.goals_scored += 1
        team2.goals_scored += 1
        team1.goals_conceded += 1
        team2.goals_conceded += 1

    return result  # Return the winner or None for a draw

# Function to update the treeview with the current rankings
def update_treeview():
    tree.delete(*tree.get_children())
    for i, team in enumerate(rankings):
        position = i + 1
        goal_difference = team.goals_scored - team.goals_conceded
        tree.insert("", "end", values=(position, team.name, team.points, team.goals_scored, team.goals_conceded, goal_difference, team.rating))

# Function to update the treeview with the games schedule and winners
def update_schedule():
    tree_schedule.delete(*tree_schedule.get_children())
    for week, matches in enumerate(schedule, start=1):
        for match in matches:
            team1, team2, winner = match.team1, match.team2, match.winner
            winner_name = winner.name if winner else "Draw"
            tree_schedule.insert("", "end", values=(week, f"{team1.name} vs. {team2.name}", winner_name))

# Function to switch between rankings and schedule views
def switch_section(section):
    if section == "Rankings":
        update_treeview()
        tree.pack(side=tk.LEFT, fill="both", expand=True)
        v_scrollbar_rankings.pack(side="right", fill="y")
        tree_schedule.pack_forget()
        v_scrollbar_schedule.pack_forget()
    elif section == "Schedule":
        update_schedule()
        tree_schedule.pack(side=tk.LEFT, fill="both", expand=True)
        v_scrollbar_schedule.pack(side="right", fill="y")
        tree.pack_forget()
        v_scrollbar_rankings.pack_forget()

# Create a list of Team objects and initialize with 64 teams with numbered names
teams = [Team(f"Team {i + 1}", random.randint(1000, 2000)) for i in range(64)]

# Simulate matches for the entire league with a schedule
weeks = 63
matches_per_week = 32  # Each team plays one match per week
schedule = []  # Store the schedule for each week

for week in range(weeks):
    matches = []
    for match_num in range(matches_per_week):
        team1 = teams[match_num]
        team2 = teams[63 - match_num]
        winner = simulate_match(team1, team2)
        matches.append(Match(team1, team2, winner))
    schedule.append(matches)

# Calculate rankings by sorting the teams based on their points, goals scored, and goal difference
rankings = sorted(teams, key=lambda x: (x.points, x.goals_scored - x.goals_conceded, x.rating), reverse=True)

# Create a GUI to display the final rankings and schedule
root = tk.Tk()
root.title("Football League")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to fit 80% of the screen
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)

# Center the window on the screen
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the window attributes
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create a frame for the rankings and schedule section
frame = ttk.Frame(root)
frame.pack(side=tk.LEFT, fill="both", expand=True)

# Create a treeview to display the rankings
tree = ttk.Treeview(frame, columns=("Position", "Team", "Points", "Goals Scored", "Goals Conceded", "Goal Difference", "Rating"), show="headings")

# Add column headings for rankings
tree.heading("Position", text="Position")
tree.heading("Team", text="Team")
tree.heading("Points", text="Points")
tree.heading("Goals Scored", text="Goals Scored")
tree.heading("Goals Conceded", text="Goals Conceded")
tree.heading("Goal Difference", text="Goal Difference")
tree.heading("Rating", text="Rating")

# Set column widths for rankings view
column_widths = [80, 150, 80, 100, 120, 130, 80]
for i, width in enumerate(column_widths):
    tree.column(i, width=width, anchor=tk.CENTER)

# Create vertical scrollbar for rankings
v_scrollbar_rankings = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=v_scrollbar_rankings.set)

# Create a treeview to display the schedule
tree_schedule = ttk.Treeview(frame, columns=("Week", "Match", "Winner"), show="headings")

# Add column headings for schedule
tree_schedule.heading("Week", text="Week")
tree_schedule.heading("Match", text="Match")
tree_schedule.heading("Winner", text="Winner")

# Set column widths for schedule view
column_widths_schedule = [80, 300, 150]
for i, width in enumerate(column_widths_schedule):
    tree_schedule.column(i, width=width, anchor=tk.CENTER)

# Create vertical scrollbar for schedule
v_scrollbar_schedule = ttk.Scrollbar(frame, orient="vertical", command=tree_schedule.yview)
tree_schedule.configure(yscrollcommand=v_scrollbar_schedule.set)

# Create buttons to switch between rankings and schedule views
button_rankings = tk.Button(root, text="Rankings", command=lambda: switch_section("Rankings"))
button_schedule = tk.Button(root, text="Schedule", command=lambda: switch_section("Schedule"))

# Pack buttons to make them visible
button_rankings.pack(side=tk.TOP, pady=10)
button_schedule.pack(side=tk.TOP, pady=10)

# Initially show the rankings view
switch_section("Rankings")

# Run the GUI
root.mainloop()
