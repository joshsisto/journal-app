import openai
import os
import glob
from datetime import datetime

from utilities import get_today, get_now, red, blue, bold 

openai.api_key = os.getenv('OPENAI_API_KEY')

with open('./prompts/assistant_prompt.txt', 'r') as f:
    assistant_prompt = f.read()

with open('./prompts/assistant_prompt_previous.txt', 'r') as f:
    assistant_prompt_previous = f.read()


def get_all_conversations():
    list_of_files = sorted(glob.glob('./logs/*/*.journal'), key=os.path.getctime)
    all_messages = []
    for file in list_of_files:
        print(f"\nLoading conversation from file: {file}")

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
        print(f"Adding the following messages for file {file}:")
        for message in messages:
            print(f"{message['role'].capitalize()}: {message['content']}")
        #append the prompt accounting for the previous conversations
        messages.append({"role": "system", "content": assistant_prompt_previous})
        all_messages.extend(messages)
    return all_messages


def generate_response_and_log(f, messages):
    print("\nSending the following messages to the assistant:")
    for message in messages:
        print(f"{message['role'].capitalize()}: {message['content']}")
        
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



def chatbot():
    messages = get_all_conversations()

    if not messages:
        messages = [
            {"role": "system", "content": assistant_prompt},
            # {"role": "user", "content": "Let me know you are ready to go."},
        ]

    timestamp_start = datetime.now()
    timestamp_str = timestamp_start.strftime("%Y-%m-%d_%H-%M-%S")

    filename = f'./logs/{get_today()}/{timestamp_str}.journal'

    with open(filename, 'w') as f:
        f.write(f"Conversation started at: {timestamp_str}\n\n")

        if messages:
            generate_response_and_log(f, messages)

        while True:
            user_message = input(bold(red("You: ")))

            if user_message.lower() == "quit":
                timestamp_end = datetime.now()
                f.write(f"\nConversation ended at: {timestamp_end.strftime('%Y-%m-%d_%H-%M-%S')}")
                duration = timestamp_end - timestamp_start
                f.write(f"\nDuration of conversation: {str(duration)}\n")
                break

            messages.append({"role": "user", "content": user_message})
            f.write("You: " + user_message + "\n\n")

            generate_response_and_log(f, messages)
