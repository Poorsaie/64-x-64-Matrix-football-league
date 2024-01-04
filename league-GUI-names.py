import random
import tkinter as tk
from tkinter import ttk
from faker import Faker

# Initialize the Faker generator
fake = Faker()

# Define a Team class to represent a football team
class Team:
    def __init__(self, name, rating):
        self.name = name
        self.rating = float(rating)
        self.points = 0
        self.goals_scored = 0
        self.goals_conceded = 0

# Function to simulate a match between two teams
def simulate_match(team1, team2):
    rating_diff = team1.rating - team2.rating
    win_probability = 1 / (1 + 10 ** (-rating_diff / 400))
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

# Function to update the treeview with the current rankings
def update_treeview():
    tree.delete(*tree.get_children())
    for i, team in enumerate(rankings):
        position = i + 1
        goal_difference = team.goals_scored - team.goals_conceded
        tree.insert("", "end", values=(position, team.name, team.points, team.goals_scored, team.goals_conceded, goal_difference, team.rating))

# Create a list of Team objects and initialize with 64 teams with random names
teams = [Team(fake.word(), random.randint(1000, 2000)) for _ in range(64)]

# Simulate matches for the entire league with a schedule
weeks = 63
matches_per_week = 32
for week in range(weeks):
    for match_num in range(matches_per_week):
        team1 = teams[match_num]
        team2 = teams[63 - match_num]
        simulate_match(team1, team2)

# Calculate rankings by sorting the teams based on their points, goals scored, and goal difference
rankings = sorted(teams, key=lambda x: (x.points, x.goals_scored - x.goals_conceded, x.rating), reverse=True)

# Create a GUI to display the final rankings
root = tk.Tk()
root.title("Football League Rankings")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to fit the screen
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)

# Center the window on the screen
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the window attributes
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create a treeview to display the rankings
tree = ttk.Treeview(root, columns=("Position", "Team", "Points", "Goals Scored", "Goals Conceded", "Goal Difference", "Rating"), show="headings")

# Add column headings
columns = ("Position", "Team", "Points", "Goals Scored", "Goals Conceded", "Goal Difference", "Rating")
for i, column in enumerate(columns):
    tree.heading(column, text=column)
    tree.column(i, width=80, anchor=tk.CENTER)

# Populate the treeview with data
update_treeview()

# Function to close the application
def close_app():
    root.destroy()

# Create a close button
close_button = tk.Button(root, text="Close", command=close_app)
close_button.pack()

# Pack the treeview to make it visible
tree.pack(fill="both", expand=True)

# Run the GUI
root.mainloop()
