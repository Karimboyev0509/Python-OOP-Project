import random
import csv
import json
from abc import ABC, abstractmethod



class PlayerState(ABC):

    @abstractmethod
    def performance_multiplier(self):
        pass

    @abstractmethod
    def state_name(self):
        pass

#Good Form State
class GoodFormState(PlayerState):
    def performance_multiplier(self):
        return 1.5
    
    def state_name(self):
        return "Good Form"
    
#Normal Form State
class NormalFormState(PlayerState):
    def performance_multiplier(self):
        return 1.0
    
    def state_name(self):
        return "Normal Form"
    
#Bad Form State
class BadFormState(PlayerState):
    def performance_multiplier(self):
        return 0.5
    
    def state_name(self):
        return "Bad Form"
    



class Person:
    def __init__(self, name):
        self.name = name

class Statistics:
    def __init__(self):
        self.matches_played = 0
        self.wins = 0
        self.losses = 0
        self.goals = 0
        self.points = 0

class Player(Person, Statistics):
    def __init__(self, name):
        Person.__init__(self, name)
        Statistics.__init__(self)
        
        self.state = NormalFormState()
    
    def score_goal(self):
        self.goals += 1

    def add_win(self):
        self.wins += 1
        self.points += 3

    def add_loss(self):
        self.losses += 1

    def info(self):
        return {
            "name": self.name,
            "matches": self.matches_played,
            "wins": self.wins,
            "lossses": self.losses,
            "goals": self.goals,
            "points": self.points,
            "state": self.state.state_name()
        }
    


class Referee:
    def __init__(self, name, experience):
        self.name = name
        self.experience = experience

    def start_match(self):
        print(f"Referee {self.name} started the match")

    def end_match(self):
        print(f"Referee {self.name} ended the match")


class Match:
    def __init__(self, player1, player2, referee):
        self.player1 = player1
        self.player2 = player2
        self.referee = referee

        self.score1 = 0
        self.score2 = 0

        self.winner = None

    def play_match(self):
        
        self.referee.start_match()

        self.player1.matches_played += 1
        self.player2.matches_played += 1

        if self.score1 > self.score2:
            self.winner = self.player1
            self.player1.add_win()
            self.player2.add_loss()
        elif self.score2 > self.score1:
            self.winner = self.player2
            self.player1.add_win()
            self.player2.add_loss()

        self.referee.end_match()

        self.log_match()
    def log_match(self):
    
        with open("matches.csv", "a", newline="") as file:
            writer = csv.writer(file)   #CSV writer tool yaratilyabti

            writer.writerow([
                self.player1.name,
                self.player2.name,
                self.score1,
                self.score2,
                self.winner.name if self.winner else "Draw"
            ])


class TournamentStrategy(ABC):

    @abstractmethod
    def schedule_matches(self, players):
        pass
        
#Round Robin Strategy-- Hamma hamma bilan.
class RoundRobinStrategy(TournamentStrategy):

    def schedule_matches(self, players):
        matches = []

        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                matches.append((players[i], players[j]))

        return matches  
    
#Knockout Strategy - Yutqazgan chiqib ketadi.
class KnockoutStrategy(TournamentStrategy):

    def schedule_matches(self, players):
        
        matches = []

        shuffled_players = players[:]
        random.shuffle(shuffled_players)

        for i in range(0, len(shuffled_players), 2):
                matches.append((
                    shuffled_players[i],
                    shuffled_players[i+1]
                ))

        return matches
    

class Tournament:
    def __init__(self, name, strategy):

        self.name = name
        self.players = []
        self.matches = []

        self.strategy = strategy
        
    def add_player(self, player):
        self.players.append(player)

    def change_strategy(self, strategy):
        self.strategy = strategy
    
    def randomize_player_forms(self):

        for player in self.players:

            state = random.choice([
                GoodFormState(),
                NormalFormState(),
                BadFormState()
            ])
            player.change_state(state)

    def schedule_matches(self):

        scheduled = self.strategy.schedule_matches(self.players)

        referee = Referee("John", 5)

        for p1, p2 in scheduled:
            match = Match(p1, p2, referee)
            self.matches.append(match)

    def start_tournament(self):
        print(f"Tournament {self.name} started")

        self.randomize_player_forms()

        self.schedule_matches()

        for match in self.matches:
            match.play_match()
    
    def show_table(self):

        sorted_players = sorted(
            self.players,
            key=lambda p: p.points,
            reverse=True
        )

        print("\n Tournament Table")

        for player in sorted_players:
            print(player.info())
        
    def generate_awards(self):

        top_scorer = max(self.players, key=lambda p: p.goals)
        best_player = max(self.players, key=lambda p: p.points)

        print("\nAwards")
        print(f"Top Scorer: {top_scorer.name}")
        print(f"Best Player: {best_player.name}")

    def export_json(self):

        data = []

        for player in self.players:
            data.append(player.info())

        with open("tournament_table.json","w") as file:
            json.dump(data, file, indent=4)

        print("Tournament table exported to Json")



class AdminCLI:

    def __init__(self):
        self.tournament = None

    def run(self):
        while True:

            print("\n1. Create Tournament")
            print("2. Add Player")
            print("3. Start Tournament")
            print("4. Show Table")
            print("5. Generate Awards")
            print("6. Export JSON")
            print("7. Exit")

            choice = input("Choose: ")

            if choice == "1":

                t_name = input("Tournament name: ")

                print("1. Round Robin")
                print("2. Knockout")

                strategy_choice = input("Choose strategy: ")

                if strategy_choice == "1":
                    strategy = RoundRobinStrategy()
                else:
                    strategy = KnockoutStrategy()
                self.tournament = Tournament(t_name, strategy)
            

            elif choice == "2":
                name = input("Player name: ")
                player = Player(name)

                self.tournament.add_player(player)
            elif choice == "3":
                self.tournament.start_tournament()

            elif choice == "4":
                self.tournament.show_table()

            elif choice == "5":
                self.tournament.generate_awards()
            elif choice == "6":
                self.tournament.export_json()
            elif choice == "7":
                break


cli = AdminCLI()
cli.run()