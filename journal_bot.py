import openai
import os
from datetime import datetime

from utilities import get_today, get_now, red, blue, bold 

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_prompt_and_conversation():
    # Load prompt
    with open('./prompts/assistant_prompt.txt', 'r') as f:
        assistant_prompt = f.read()

    # Load .all file
    all_file_path = f"./logs/{get_today()}/{get_today()}.all"
    with open(all_file_path, 'r') as f:
        all_conversation = f.read()

    # Concatenate the prompt and the conversation
    conversation = assistant_prompt + "\n" + all_conversation
    return conversation

def chatbot():
    # Get the combined prompt and conversation
    conversation = get_prompt_and_conversation()

    # Create an initial system message with the conversation
    messages = [
        {"role": "system", "content": conversation},
    ]

    timestamp_start = datetime.now()
    timestamp_str = timestamp_start.strftime("%Y-%m-%d_%H-%M-%S")

    filename = f'./logs/{get_today()}/{timestamp_str}.journal'

    with open(filename, 'w') as f:
        f.write(f"Conversation started at: {timestamp_str}\n\n")

        # Send the messages to the assistant and get the response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
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
        print("Assistant: ", blue(assistant_message))

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

            # Send the messages to the assistant and get the response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k-0613",
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
            print("Assistant: ", blue(assistant_message))
