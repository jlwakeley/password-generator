#!/usr/bin/env python3

import secrets
import string

import pyperclip


# Function to generate the password
def generate_password(excluded_symbols, length):
    """
    Generate a password with the given length and excluded symbols
    """
    char_symb = string.ascii_letters + string.digits + string.punctuation
    for char in excluded_symbols:
        char_symb = char_symb.replace(char, "")
    if not char_symb:
        raise ValueError(
            "All symbols, numbers, and letters are excluded. Please try again."
        )
    return "".join(secrets.choice(char_symb) for i in range(length))


# Function to get user input for excluded symbols and password length
def get_user_input():
    """
    Get user input for excluded symbols and password length
    """
    while True:
        excluded_symbols = input("Exclude what symbols? ")
        length_str = input("Length requirement? ")
        try:
            length = int(length_str)
            if length <= 0:
                print("Must input a length requirement")
                continue
            return excluded_symbols, length
        except ValueError:
            print("Must input a length requirement")
            continue


# Main loop
def main():
    while True:
        print(
            """
        <<<<<<<<<<<<<<<<<< Password Generator >>>>>>>>>>>>>>>>>>
        """
        )

        # Get user input
        excluded_symbols, length = get_user_input()

        # Generate password
        try:
            password = generate_password(excluded_symbols, length)
        except ValueError:
            print("All symbols, numbers, and letters are excluded. Please try again.")
            continue

        # Print password and copy it to clipboard
        print(f"New password: {password}")
        pyperclip.copy(password)

        # Ask if the user wants to generate another password
        answer = input("Generate another password? (y/n): ")
        if answer.lower() != "y":
            print("Have a good day!")
            break


if __name__ == "__main__":
    main()
