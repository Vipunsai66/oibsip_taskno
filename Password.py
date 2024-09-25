import random
import string

# Function to generate random password
def generate_password(length, use_uppercase=True, use_digits=True, use_special=True):
    # Basic characters: lowercase letters
    characters = list(string.ascii_lowercase)
    
    # Optionally add uppercase letters
    if use_uppercase:
        characters.extend(string.ascii_uppercase)
    
    # Optionally add digits
    if use_digits:
        characters.extend(string.digits)
    
    # Optionally add special characters
    if use_special:
        characters.extend(string.punctuation)
    
    # Ensure there's a mix of all character types
    password = [
        random.choice(string.ascii_lowercase),  # Ensure at least one lowercase
    ]
    
    if use_uppercase:
        password.append(random.choice(string.ascii_uppercase))  # Ensure at least one uppercase
    
    if use_digits:
        password.append(random.choice(string.digits))  # Ensure at least one digit
    
    if use_special:
        password.append(random.choice(string.punctuation))  # Ensure at least one special char
    
    # Fill the rest of the password
    for _ in range(length - len(password)):
        password.append(random.choice(characters))
    
    # Shuffle to avoid predictable placement
    random.shuffle(password)
    
    # Convert list to string and return
    return ''.join(password)

# User input for password length and options
def get_user_options():
    try:
        length = int(input("Enter the password length (minimum 4): "))
        if length < 4:
            print("Password length must be at least 4. Setting to 8 by default.")
            length = 8
        
        use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
        use_digits = input("Include digits? (y/n): ").lower() == 'y'
        use_special = input("Include special characters? (y/n): ").lower() == 'y'

        return length, use_uppercase, use_digits, use_special
    except ValueError:
        print("Invalid input! Please enter numeric values for length.")
        return get_user_options()

# Main function to run the program
def main():
    print("Welcome to the Random Password Generator!")

    length, use_uppercase, use_digits, use_special = get_user_options()

    password = generate_password(length, use_uppercase, use_digits, use_special)

    print(f"Generated Password: {password}")

if __name__ == "__main__":
    main()
