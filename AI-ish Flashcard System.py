import json
import csv
import logging
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

logging.basicConfig(filename="session.log", level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s")


class Card:
    def __init__(self, question, answer, difficulty):
        self.question = question
        self.answer = answer
        self.difficulty = difficulty
        self.success = 0
        self.attempts = 0

        self.next_review = datetime.now()

    @property
    def success_rate(self):

        if self.attempts == 0:
            return 0
        return round((self.success / self.attempts) * 100, 2)



class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)


class User:
    def __init__(self, name):
        self.name = name
        self.correct_answers = 0
        self.wrong_answers = 0


class RepetitionStrategy(ABC):
    @abstractmethod
    def calculate_next_review(self, card, correct):
        pass


class SM2Strategy(RepetitionStrategy):
    def calculate_next_review(self, correct):
        if correct:
            interval = 6
        else:
            interval = 1
        return datetime.now() + timedelta(days=interval)


class Session:
    def __init__(self, user, deck, strategy):
        self.user = user
        self.deck = deck
        self.strategy = strategy
    
    def start_quiz(self):
        print(f"Starting Quiz for {self.user.name}")
        
        for card in self.deck.cards:
            if datetime.now() < card.next_review:
                continue
            print("\nQuestion:")
            print(card.question)

            answer = input("Answer: ")
            card.attempts += 1

            if answer.lower() == card.answer.lower():
                print("Correct!")

                self.user.correct_answers += 1
                card.success += 1
                correct = True

                logging.info(f"{self.user.name} answered correctly: {card.question}")
            else:
                print("Wrong!")
                print("Correct answer:", card.answer)

                self.user.wrong_answers += 1
                correct = False
                logging.info(f"{self.user.name} answered wrong: {card.question}")


            card.next_review = self.strategy.calculate_next_review(card, correct)

    def hardest_cards(self):
        hardest = sorted(self.deck.cards, key=lambda card: card.success_rate)
        print("\nHardest Cards:")

        for card in hardest[:3]: #eng past ishlangan 3 ta card
            print(f"{card.question} , Success Rate: {card.success_rate}%")

    def top_topics(self):
        sorted_cards = sorted(self.deck.cards, key=lambda card: card.success,
            reverse=True)

        print("\nTop Learned Topics:")
        for card in sorted_cards[:3]:
            print( f"{card.question} , Correct: {card.success}")

    def save_json(self):
        data = []
        for card in self.deck.cards:
            info = {"question": card.question,"success_rate": card.success_rate,
                "attempts": card.attempts}

            data.append(info)

        with open("flashcards.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Json saved")

    def save_csv(self):
        with open("flashcards.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Question","Success Rate","Attempts"])

            for card in self.deck.cards:
                writer.writerow([card.question, card.success_rate, card.attempts])

        print("CSV saved")

deck = Deck("Python Deck")

card1 = Card("OOP nima?", "Object Oriented Programming", 2)

card2 = Card("Inheritance nima?","Voris olish", 3)

card3 = Card("Polymorphism nima?", "Child class parent methodni o'zgartirib yozish", 4)

deck.add_card(card1)
deck.add_card(card2)
deck.add_card(card3)

user = User("Muhammadkarim")

strategy = SM2Strategy()

session = Session(user, deck,strategy)

session.start_quiz()
session.hardest_cards()
session.top_topics()
session.save_json()
session.save_csv()

print("Quiz Finished")
print("Correct:", user.correct_answers)
print("Wrong:", user.wrong_answers)
