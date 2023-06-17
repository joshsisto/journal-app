import datetime
import os

from utilities import get_today


def get_last_journal_date():
    journal_files = sorted([f for f in os.listdir() if f.endswith('.txt')], key=os.path.getmtime)
    if journal_files:
        most_recent_file = journal_files[-1]
        return datetime.datetime.fromtimestamp(os.path.getmtime(most_recent_file))
    else:
        return None


def create_journal_entry():
    try:
        filename = f"{get_today()}.txt"
        with open(filename, 'w') as file:
            file.write(f"{datetime.datetime.now().ctime()}\n\n")
            response = input("Write your journal entry: ")
            file.write(f"{response}\n")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")


def guided_journal_entry():
    try:
        last_journal_date = get_last_journal_date()
        filename = f"{get_today()}.txt"
        with open(filename, 'w') as file:
            file.write(f"{datetime.datetime.now().ctime()}\n\n")
            if last_journal_date is not None:
                hours_since_last_journal = (datetime.datetime.now() - last_journal_date).total_seconds() / 3600
                if hours_since_last_journal > 20:
                    days_since_last_journal = hours_since_last_journal // 24
                    welcome_back_question = f"Welcome back! It's been {int(days_since_last_journal)} days since you journaled. What's happened since your last entry on {last_journal_date.strftime('%Y-%m-%d')}?"
                    print(welcome_back_question)
                    response = input("Your response: ")
                    file.write(f"{welcome_back_question}\n")
                    file.write(f"Response: {response}\n\n")

            questions = ["How are you feeling?", "Where are you writing this?", "Tell me about your day", "Anything else you would like to discuss?"]

            if datetime.datetime.now().hour < 18:  # If it's before 6PM, ask about today's goals
                questions.append("What are your goals for the day?")

            for i, question in enumerate(questions, 1):
                print(f"{i}. {question}")
                response = input("Your response: ")
                file.write(f"{question}\n")
                file.write(f"Response: {response}\n\n")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")



def read_journal_entry():
    try:
        journals = [file for file in os.listdir() if file.endswith('.txt')]
        assert journals, "No journal entries found."
        for i, journal in enumerate(journals):
            print(f"{i+1}. {journal}")
        while True:
            choice = int(input("Select a journal to read: ")) - 1
            if 0 <= choice < len(journals):
                break
            else:
                print("Invalid choice. Please choose a valid number.")
        with open(journals[choice], 'r') as file:
            print(file.read())
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
    except AssertionError as e:
        print(e)