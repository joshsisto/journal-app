# Journal-App

This is a guided journaling application developed by Josh Sisto. The application is written in Python and is composed of several key components. Here's an overview of the functionalities provided by the different Python files:

## journal.py

This file contains the core functionality for creating and reading journal entries. Here are the primary methods:

- `get_last_journal_date()`: This function finds the date of the most recent journal entry.
- `create_journal_entry()`: This function creates a new journal entry, prompting the user for their input.
- `guided_journal_entry()`: This function guides the user through creating a journal entry by asking a series of questions. The questions asked vary based on the time of day and how long it's been since the user's last journal entry.
- `read_journal_entry()`: This function provides a list of all journal entries for the current day and allows the user to select one to read.

## journal_bot.py

This file uses OpenAI's GPT-3 model to interact with the user. It loads conversations from previous journal entries and uses them as context for the chat model. It also formats and prints the interactions between the user and the chat model. Here's a brief overview of some of the key functions:

- `get_all_conversations()`: This function retrieves all journal entries and prepares them for use as context for the chat model.
- `chatbot()`: This function manages the chat session with the user. It keeps track of all messages exchanged during the session, sends user messages to the GPT-3 model, and handles the model's responses.

## main.py

This file presents a menu to the user and calls the appropriate functions based on the user's choice. There appear to be four options:

1. Read a journal entry
2. Create a journal entry
3. Create a guided journal entry
4. Use the chatbot

### Showing Erik how Git works
