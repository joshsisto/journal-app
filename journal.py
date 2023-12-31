import datetime
import os

from utilities import get_now, get_today

# create the directory if it doesn't exist
os.makedirs(f'./logs/{get_today()}', exist_ok=True)

def get_last_journal_date():
    journal_files = []
    for root, dirs, files in os.walk('./logs'):  
        for file in files:
            if file.endswith('.journal'):
                journal_files.append(os.path.join(root, file))
    
    # Sort based on the names (timestamps) of the files
    journal_files = sorted(journal_files)
    
    if journal_files:
        most_recent_file = journal_files[-1]
        # Extract the timestamp from the filename and convert it to a datetime object
        timestamp_str = os.path.basename(most_recent_file).replace('.journal', '').replace('T', ' ')
        last_modified_time = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return last_modified_time, most_recent_file
    else:
        return None, None

def read_journal_entry():
    try:
        journal_files = []
        for root, dirs, files in os.walk('./logs'):
            for file in files:
                if file.endswith('.all'):
                    journal_files.append(os.path.join(root, file))

        assert journal_files, "No journal entries found."
        for i, journal in enumerate(journal_files):
            print(f"{i+1}. {os.path.basename(journal)}")  # Use os.path.basename to print only the filename
        while True:
            choice = int(input("Select a journal to read: ")) - 1
            if 0 <= choice < len(journal_files):
                break
            else:
                print("Invalid choice. Please choose a valid number.")
        with open(journal_files[choice], 'r') as file:
            print(file.read())
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
    except AssertionError as e:
        print(e)

def create_journal_entry():
    try:
        filename = f"{get_now()}.journal"
        with open(f'./logs/{get_today()}/' + filename, 'w') as file:
            file.write(f"{datetime.datetime.now().ctime()}\n\n")
            response = input("Write your journal entry: ")
            file.write(f"{response}\n")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

def guided_journal_entry():
    try:
        last_journal_date, last_journal_path = get_last_journal_date()
        # print("Last journal date:", last_journal_date)
        # print("Last journal path:", last_journal_path)
        filename = f"{get_now()}.journal"
        goals_asked_file = f'./logs/{get_today()}/goals_asked.goals'
        with open(f'./logs/{get_today()}/' + filename, 'w') as file:
            file.write(f"{datetime.datetime.now().ctime()}\n\n")
            if last_journal_date is not None:
                hours_since_last_journal = (datetime.datetime.now() - last_journal_date).total_seconds() / 3600
                days_since_last_journal = hours_since_last_journal // 24

                # If there is no journal entry for the previous day or more
                if days_since_last_journal > 1:
                    # If there are no entries for more than 4 days
                    if days_since_last_journal > 4:
                        welcome_back_question = f"Welcome back! It's been {int(days_since_last_journal)} days since you journaled. What's happened since your last entry on {last_journal_date.strftime('%Y-%m-%d')}?"
                        print(welcome_back_question)
                        response = input("Your response: ")
                        file.write(f"Question: {welcome_back_question}\n")
                        file.write(f"Response: {response}\n\n")
                    else:
                        # Ask about each day that is missing
                        for i in range(1, int(days_since_last_journal) + 1):
                            # Convert the string to datetime.date object
                            today_date = datetime.datetime.strptime(get_today(), '%Y-%m-%d').date()
                            missed_day_question = f"What did you do on {today_date - datetime.timedelta(days=i)}?"
                            print(missed_day_question)
                            response = input("Your response: ")
                            file.write(f"Question: {missed_day_question}\n")
                            file.write(f"Response: {response}\n\n")

                # Check if there are any journal entries today
                today_files = os.listdir(f'./logs/{get_today()}')
                today_journal_files = [file for file in today_files if file.endswith('.journal')]
                # print("Today's journal files:", today_journal_files)

                # If the current journal entry is the first of the day and the last journal was before 8PM the previous day
                if days_since_last_journal == 1 and last_journal_date.hour < 20:
                    print("Condition passed.")
                    evening_question = f"I see your last journal entry was {last_journal_date.strftime('%Y-%m-%d at %I:%M %p')}. Tell me about the rest of your day or evening."
                    print(evening_question)
                    response = input("Your response: ")
                    file.write(f"Question: {evening_question}\n")
                    file.write(f"Response: {response}\n\n")                

            questions = ["How are you feeling?", "Where are you writing this?", "Tell me about your day", "Anything else you would like to discuss?"]

            if datetime.datetime.now().hour < 18 and not os.path.exists(goals_asked_file):  # If it's before 6PM and goals question has not been asked today
                goals_question = "What are your goals for the day?"
                questions.append(goals_question)

            for i, question in enumerate(questions, 1):
                print(f"{i}. {question}")
                response = input("Your response: ")
                file.write(f"Question: {question}\n")
                file.write(f"Response: {response}\n\n")

                # If the goals question was asked, create the goals_asked.goals file and write the response
                if question == "What are your goals for the day?":
                    with open(goals_asked_file, 'w') as ga_file:
                        ga_file.write(f"Goals for the day: {response}")

    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

def consolidate_files():
    try:
        consolidated_filename = f"./logs/{get_today()}/{get_today()}.all"
        file_types = ['.stats', '.todo', '.journal', '.goals']

        # Create or overwrite the consolidated file
        with open(consolidated_filename, 'w') as consolidated_file:
            # Iterate over each file type
            for file_type in file_types:
                # Get a list of all files of the current type, sorted by modification time
                files = sorted([f for f in os.listdir(f'./logs/{get_today()}') if f.endswith(file_type)], key=lambda f: os.path.getmtime(f'./logs/{get_today()}/{f}'))
                # If there are no files of this type, skip to the next type
                if not files:
                    continue
                # Write the file type to the consolidated file
                consolidated_file.write(f"\n--- {file_type[1:].upper()} ---\n")
                # Iterate over each file of the current type
                for filename in files:
                    # Write the file's contents to the consolidated file
                    with open(f'./logs/{get_today()}/' + filename, 'r') as file:
                        consolidated_file.write(file.read())
    except IOError as e:
        print(f"An error occurred while writing to the consolidated file: {e}")
