import threading
import json
from scrape import scrape_food, scrape_links
from database import create, print_recipes, delete_all_records, insert
from producer import send_to_kafka
from consumer import consume_from_kafka

# Global flag to control the consumer thread
running = [True]

def main():
    print("Please wait, the program has to download the data...")
    food_data = scrape_links()
    food_recipes = scrape_food(food_data)
    create()
    print('Data download complete!')

    while True:
        options = """
        [1] Insert all data
        [2] Show all data
        [3] Delete all data
        [4] Quit app 
        """
        option = input(options)
        if option == '1':
            insert_data(food_recipes)
        elif option == '2':
            print_recipes()
        elif option == '3':
            delete_all_records()
            print("All records deleted.")
        elif option == '4':
            print("Exiting the application...")
            break
        else:
            print("Invalid option. Please try again.")

def insert_data(food_recipes):
    print("Please wait, the program has to insert the data...")
    batch_size = 50
    batch = []

    for recipe in food_recipes:
        batch.append(recipe)
        if len(batch) >= batch_size:
            send_to_kafka('recipes_topic', batch)
            batch.clear()  # Clear the batch

    if batch:
        send_to_kafka('recipes_topic', batch)

    print('Data insertion complete!')

if __name__ == "__main__":
    consumer_thread = threading.Thread(target=consume_from_kafka, args=('recipes_topic', running))
    consumer_thread.start()

    try:
        main()
    finally:
        running[0] = False
        consumer_thread.join()
        print("Consumer thread has been stopped. Exiting the application.")