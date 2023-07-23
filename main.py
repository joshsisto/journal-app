from journal import create_journal_entry, guided_journal_entry, read_journal_entry, consolidate_files
from stats import create_stats_entry
from todo import manage_todo_list
from journal_bot import chatbot, summarize_all_files, weekly_summary, total_summary

def main():
    while True:
        print("\n1. New journal entry\n2. Guided journal entry\n3. Read a previous journal\n4. To-do list\n5. New stats entry\n6. chatbot\n7. Summarize\n8. weekly\n9. Life Story!\n10. Exit")
        choice = int(input("Select an option: "))
        if choice == 1:
            create_journal_entry()
            consolidate_files()
        elif choice == 2:
            create_stats_entry()
            guided_journal_entry()
            manage_todo_list()
            consolidate_files()
            chatbot()
        elif choice == 3:
            read_journal_entry()
        elif choice == 4:
            manage_todo_list()
            consolidate_files()
        elif choice == 5:
            create_stats_entry()
        elif choice == 6:
            chatbot()
            consolidate_files()
        elif choice == 7:
            summarize_all_files()
        elif choice == 8:
            weekly_summary()
        elif choice == 9:
            total_summary()
        elif choice == 10:
            break
        else:
            print("Invalid choice. Please choose a number from 1 to 7.")

if __name__ == "__main__":
    main()
