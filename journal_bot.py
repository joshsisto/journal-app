import openai
import os
import glob
from datetime import datetime

openai.api_key = os.getenv('OPENAI_API_KEY')

def bold(text):
    bold_start = "\033[1m"
    bold_end = "\033[0m"
    return bold_start + text + bold_end

def blue(text):
    blue_start = "\033[34m"
    blue_end = "\033[0m"
    return blue_start + text + blue_end

def red(text):
    red_start = "\033[31m"
    red_end = "\033[0m"
    return red_start + text + red_end

with open('./prompts/assistant_prompt.txt', 'r') as f:
    assistant_prompt = f.read()

with open('./prompts/assistant_prompt_previous.txt', 'r') as f:
    assistant_prompt_previous = f.read()

def get_all_conversations():
    list_of_files = sorted(glob.glob('./logs/*/*.journal'), key=os.path.getctime)
    all_messages = []
    for file in list_of_files:
        print(f"Loading conversation from file: {file}")

        # Extract timestamp from filename
        timestamp = os.path.basename(file).split('T')[0] + ' ' + os.path.basename(file).split('T')[1].split('.')[0]
        try:
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d_%H-%M-%S").strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

        with open(file, 'r') as f:
            content = f.read()
        messages = [
            {"role": "system", "content": f"This is an uploaded journal entry from {timestamp}.\n\n"},
            {"role": "user", "content": content},
        ]
        #append the prompt accounting for the previous conversations
        messages.append({"role": "system", "content": assistant_prompt_previous})
        all_messages.extend(messages)
    return all_messages

from utilities import get_today, get_now

def chatbot():
    messages = get_all_conversations()

    if not messages:
        messages = [
            {"role": "system", "content": assistant_prompt},
            # {"role": "user", "content": "Let me know you are ready to go."},
        ]

    # Use get_now() from utilities to get the timestamp in the format you want
    timestamp_str = get_now()

    # Save the file in the correct logs directory
    filename = f'./logs/{get_today()}/{timestamp_str}.journal'

    with open(filename, 'w') as f:
        f.write(f"Conversation started at: {timestamp_str}\n\n")

        if messages:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                temperature=0.8,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6
            )
            assistant_message = response.choices[0].message['content']
            messages.append({"role": "assistant", "content": assistant_message})
            f.write("Assistant: " + assistant_message + "\n\n")
            print(bold(blue("Assistant: ")), blue(assistant_message))

        while True:
            user_message = input(bold(red("You: ")))

            if user_message.lower() == "quit":
                timestamp_end = datetime.now()
                timestamp_end_str = timestamp_end.strftime("%Y-%m-%d_%H-%M-%S")
                f.write(f"\nConversation ended at: {timestamp_end_str}")
                duration = timestamp_end - timestamp_start
                f.write(f"\nDuration of conversation: {duration}\n")
                break

            messages.append({"role": "user", "content": user_message})
            f.write("You: " + user_message + "\n\n")

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                temperature=0.8,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6
            )

            assistant_message = response.choices[0].message['content']
            messages.append({"role": "assistant", "content": assistant_message})
            f.write("Assistant: " + assistant_message + "\n\n")
            print(bold(blue("Assistant: ")), blue(assistant_message))
