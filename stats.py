import datetime
import os
import json

from utilities import get_today

# create the directory if it doesn't exist
os.makedirs(f'./logs/{get_today()}/', exist_ok=True)

def create_stats_entry():
    try:
        filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}.stats"
        questions = {
            "What time did you go to bed last night?": {},
            "What time did you wake up this morning?": {},
            "Did you exercise today?": {"follow_up": "What did you work on?"},
            "Did you steam or sauna today?": {}
        }

        responses = {}
        if os.path.exists(f'./logs/{get_today()}/' + filename):  # Corrected this line
            with open(f'./logs/{get_today()}/' + filename, 'r') as file:
                responses = json.load(file)

        with open(f'./logs/{get_today()}/' + filename, 'w') as file:
            for question, details in questions.items():
                if question in responses and (question not in ["Did you exercise today?", "Did you steam or sauna today?"] or responses[question] == "yes"):
                    continue
                print(question)
                response = input("Your response: ")
                responses[question] = response
                if details.get("follow_up") and response.lower() == 'yes':
                    print(details["follow_up"])
                    follow_up_response = input("Your response: ")
                    responses[details["follow_up"]] = follow_up_response
            json.dump(responses, file, indent=4)
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

