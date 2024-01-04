import random

# Define a Team class to represent a football team
class Team:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.points = 0
        self.goals_scored = 0
        self.goals_conceded = 0

    def __str__(self):
        return f"{self.name} - Points: {self.points}, Rating: {self.rating}"

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

# Create a list of Team objects and initialize with 64 teams
teams = []
team_names = ["Team " + str(i) for i in range(1, 65)]
team_ratings = [random.randint(1000, 2000) for _ in range(64)]

for name, rating in zip(team_names, team_ratings):
    team = Team(name, rating)
    teams.append(team)

# Simulate matches for the entire league
for round in range(63):  # Each team plays 63 matches in a season
    print(f"Round {round + 1} Matches:")
    for i in range(round + 1):
        team1 = teams[i]
        team2 = teams[63 - i]

        simulate_match(team1, team2)
        print(f"{team1.name} vs. {team2.name}")

    print()

# Calculate rankings by sorting the teams based on their points, goals scored, and goal difference
rankings = sorted(teams, key=lambda x: (x.points, x.goals_scored - x.goals_conceded, x.rating), reverse=True)

# Display the rankings in a user-friendly format
print("Final Rankings:")
for i, team in enumerate(rankings):
    print(f"{i + 1}. {team}")

# Main program
if __name__ == "__main__":
    pass
