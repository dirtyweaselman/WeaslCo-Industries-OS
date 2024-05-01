# run in cmd.exe: python C:\Users\Weasl\PycharmProjects\Terminal\app.py
import os
import time
import random
import requests
import json
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

project_root = os.path.dirname(os.path.abspath(__file__))
pygame.init()
pygame.mixer.init()
enter = pygame.mixer.Sound(project_root + "/sounds/enter.wav")
pop = pygame.mixer.Sound(project_root + "/sounds/scroll.wav")
password_path = project_root + '/password.txt'
hacking_attempts = 4
good = pygame.mixer.Sound(project_root + "/sounds/good.wav")
bad = pygame.mixer.Sound(project_root + "/sounds/bad.wav")


def line(text, delay=0.01):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def load_words(filename):
    with open(filename, 'r') as file:
        words = json.load(file)
    # Select a random subset of 2-5 words from the list
    num_words = random.randint(2, 5)  # Choose how many words to pick
    selected_words = random.sample(words, num_words)
    return [word.upper() for word in selected_words]  # Convert all to uppercase


words = load_words(project_root + "/words.json")


def generate_grid(rows, cols, words, characters):
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    placed_words = []

    # Place words in the grid
    for word in words:
        word_placed = False
        attempts = 0  # Prevent infinite loop
        while not word_placed and attempts < 100:
            direction = random.choice(['horizontal', 'vertical'])
            if direction == 'horizontal':
                start_row = random.randint(0, rows - 1)
                start_col = random.randint(0, cols - len(word))
            else:
                start_row = random.randint(0, rows - len(word))
                start_col = random.randint(0, cols - 1)

            # Check if space is available
            if all(grid[start_row + i * (direction == 'vertical')][
                       start_col + i * (direction == 'horizontal')] == '' for i in range(len(word))):
                for i in range(len(word)):
                    grid[start_row + i * (direction == 'vertical')][start_col + i * (direction == 'horizontal')] = word[
                        i]
                word_placed = True
                placed_words.append(word)
            attempts += 1

    # Fill in remaining spaces with random characters
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '':
                grid[i][j] = random.choice(characters)

    return grid, placed_words


def hacking():
    good.play()
    global hacking_attempts
    os.system('cls' if os.name == 'nt' else 'clear')
    line("(c) 2044 Maple LLC Practice Hacking Terminal v0.1.2")
    line(f"ATTEMPT(S) LEFT: {hacking_attempts} OF 4")
    print("")

    words = load_words(project_root + "/words.json")
    characters = "!@#$%&*:[]"
    rows = 20
    cols = 20

    grid, placed_words = generate_grid(rows, cols, words, characters)
    correct_word = random.choice(placed_words)
    for row in grid:
        print(' '.join(row))

    while hacking_attempts > 0:
        guess = input("Enter your guess: ").upper()
        if guess in placed_words:
            if guess == correct_word:
                good.play()
                print("Access granted!")
                restart = input("Would you like to try again? (y/n): ")
                if restart == "y":
                    hacking_attempts = 4
                    hacking()
                else:
                    main()
                    break

                break
            else:
                good.play()
                likeness = sum(a == b for a, b in zip(guess, correct_word))
                print(f"Likeness={likeness}")
        else:
            bad.play()
            print("Word not found in grid.")

        hacking_attempts -= 1
        line(f"ATTEMPT(S) LEFT: {hacking_attempts} OF 4")

        if hacking_attempts == 0:
            bad.play()
            print("Access denied. System locked!")
            print("Please wait 15 seconds before trying again.")
            time.sleep(15)
            restart = input("Would you like to try again? (y/n): ")
            if restart == "y":
                hacking_attempts = 4
                hacking()
            else:
                main()
                break


def browser():
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    print("WeaslCo Industries Browser v0.0.2")
    print("Enter a URL to visit.")

    allowed_urls = {
        "https://drtyweasl.com/google/"
    }

    user_input = input("URL: > ")

    # Check if the entered URL is in the whitelist
    if user_input in allowed_urls:
        response = requests.get(user_input)
        print(response.text)
        user_input = input("Press enter to return to the URL select.")
        browser()
    else:
        print("Access to this URL is restricted.")


def password():
    os.system('cls' if os.name == 'nt' else 'clear')
    line("WeaslCo Industries Security Identification System v1.2.1")
    print("Enter your password to continue.")
    user_password = input("Password: ")

    # Read password from file
    with open(password_path, 'r') as file:
        stored_password = file.read().strip()  # .strip() to remove any extraneous whitespace/newlines

    if user_password == stored_password:
        print("Password accepted.")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print("Password incorrect.")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        password()  # Recursively retrying the password input


def error():
    os.system('cls' if os.name == 'nt' else 'clear')
    sound = pygame.mixer.Sound(project_root + "/sounds/bad.wav")
    sound.play()
    while pygame.mixer.get_busy():
        pygame.time.delay(100)
    time.sleep(.2)
    line("Memory Check Failed. Please restart your computer.")
    line("Automatically restarting in 5 seconds...")
    time.sleep(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    line("Restarting...")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('python ' + project_root + '/app.py')


# Programs
def word():
    project_root = os.path.dirname(os.path.abspath(__file__))
    print("WeaslCo Word Processor v1.0.0")
    print("Commands: type, exit")
    print("Type 'exit' to return to the main menu.")
    while True:
        user_input = input("W:\ > ")
        if user_input == "exit":
            print("Exiting Word Processor...")
            main()
            break
        elif user_input == "type":
            user_input = input("Enter file name: ")
            name = user_input
            print("Start typing your text. Press enter on an empty line to save and exit.")
            text_to_save = ""
            while True:
                line = input()
                if line.strip() == "":
                    break
                text_to_save += line + "\n"

            file_path = os.path.join(project_root, name + '.txt')
            with open(file_path, 'w') as file:
                file.write(text_to_save)
        else:
            print(f"Command '{user_input}' not recognized.")


def mail():
    project_root = os.path.dirname(os.path.abspath(__file__))
    print("WeaslCo Mail v1.0.0")
    print("Commands: send, read, exit")
    print("Type 'exit' to return to the main menu.")

    while True:
        user_input = input("M:\ > ")
        if user_input == "exit":
            print("Exiting Mail...")
            main()
            break
        elif user_input == "send":
            pop.play()
            user_input = input("Enter recipient: ")
            recipient = user_input
            user_input = input("Enter subject: ")
            subject = user_input
            print("Start typing your email. Press enter on an empty line to send.")
            text_to_send = ""
            while True:
                line = input()
                if line.strip() == "":
                    break
                text_to_send += line + "\n"

            file_path = os.path.join(project_root, 'outbox.txt')
            with open(file_path, 'a') as file:
                file.write(f"To: {recipient}\n")
                file.write(f"Subject: {subject}\n")
                file.write(text_to_send)
                file.write("\n")
        elif user_input == "read":
            pop.play()
            print("Read inbox or outbox?")
            user_input = input("Enter inbox or outbox: ")
            if user_input == "inbox":
                pop.play()
                file_path = os.path.join(project_root, 'inbox.txt')
                with open(file_path, 'r') as file:
                    print(file.read())
            elif user_input == "outbox":
                pop.play()
                file_path = os.path.join(project_root, 'outbox.txt')
                with open(file_path, 'r') as file:
                    print(file.read())
        else:
            print(f"Command '{user_input}' not recognized.")


home = ["exit", "word", "mail", "browser"]

os.system('cls' if os.name == 'nt' else 'clear')
pygame.mixer.music.load(project_root + "/sounds/fan.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
sound = pygame.mixer.Sound(project_root + "/sounds/buttonstart.wav")
sound.play()
while pygame.mixer.get_busy():
    pygame.time.delay(100)
time.sleep(1.5)
sound = pygame.mixer.Sound(project_root + "/sounds/bad.wav")
sound.play()
while pygame.mixer.get_busy():
    pygame.time.delay(100)


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("__        __             _  ____      ")
    print("\ \      / /__  __ _ ___| |/ ___|___  ")
    print(" \ \ /\ / / _ \/ _` / __| | |   / _ \ ")
    print("  \ V  V /  __/ (_| \__ \ | |__| (_) |")
    print("   \_/\_/ \___|\__,_|___/_|\____\___/ ")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')

    line("=============================================================================")
    line("====================(c) Copyright 2045 WeaslCo Industries====================")
    line("=============================================================================")
    line("Loading WeaslCo Industries OS v1.3.6...")
    line("Memory Check: 0%")
    line("Memory Check: 10%")
    line("Memory Check: 67%")
    line("Memory Check: 100%")
    if random.random() < 0.85:
        line("Memory Check Found 8192KB of RAM")
        line("Loading Kernel...")
        time.sleep(random.uniform(1.5, 5.5))
        line("Kernel Loaded Successfully")
        line("Loading User Interface...")
        time.sleep(random.uniform(1.5, 5.5))
        line("User Interface Loaded Successfully")
        line("Connecting to servers...")
        time.sleep(random.uniform(1.5, 5.5))
        line("Connected to servers.")
        time.sleep(random.uniform(1.5, 5.5))
        sound = pygame.mixer.Sound(project_root + "/sounds/good.wav")
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.delay(100)

        os.system('cls' if os.name == 'nt' else 'clear')

        password()

        line("====================(c) Copyright 2045 WeaslCo Industries====================")
        line("=============================================================================")
        line("Welcome to WeaslCo Industries OS v1.3.6 - Connected to servers.")
        line("Current commands: word, mail, browser, hp (hackpractice), exit")
        while True:
            user_input = input("A:\ > ")
            if user_input not in home:
                enter.play()
                print(f"Command '{user_input}' not recognized.")
            if user_input == "exit":
                print("Closing Operating System. Goodbye!")
                break
            elif user_input == "word":
                enter.play()
                print("Opening Word Processor...")
                time.sleep(2.35)
                word()
            elif user_input == "mail":
                enter.play()
                print("Opening Mail...")
                mail()
            elif user_input == "browser":
                enter.play()
                print("Opening Browser...")
                time.sleep(7.352)
                browser()
            elif user_input == "hp" or user_input == "hackpractice":
                enter.play()
                hacking()

    else:
        error()


main()
