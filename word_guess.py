import random
import time

def get_word():
    """Returns random word."""
    words = ['Charlie', 'Woodstock', 'Snoopy', 'Lucy', 'Linus',
             'Schroeder', 'Patty', 'Sally', 'Marcie']
    return random.choice(words).upper()

def check(word, guesses):
    """Creates and returns string representation of word
    displaying asterisks for letters not yet guessed."""
    status = '' # Current status of guess
    last_guess = guesses[-1]
    matches = 0 # Number of occurrences of last_guess in word

    for L in word:
    # Loop through word checking if each letter is in guesses
        if guesses.count(L) > 0:
    #  If it is, append the letter to status
            status += L
    #  If it is not, append an asterisk (*) to status
        else:
            status += "*"
    # Also, each time a letter in word matches the last guess,
        if L == last_guess:
    #  increment matches by 1.
            matches += 1

    print("\n{}".format(status))
    # Write a condition that outputs one of the following when
    #  the user's last guess was "A":
    if last_guess == "A":
        match matches:
    #   'The word has 2 "A"s.' (where 2 is the number of matches)
            case 2:
                print("The word has two \"A\"s.")
    #   'The word has one "A".'
            case 1:
                print("The word has one \"A\".")
    #   'Sorry. The word has no "A"s.'
            case other:
                print("Sorry, The word has no \"A\"s.")

    return status

def main():
    random.seed(time.time())
    word = get_word() # The random word
    n = len(word) # The number of letters in the random word
    guesses = [] # The list of guesses made so far
    guessed = False
    print("\nWord Guess\n")
    print('The word contains {} letters.'.format(n))

    while not guessed:
        guess = input('Guess a letter or a {}-letter word: '.format(n))
        guess = guess.upper()
        # Write an if condition to complete this loop.
        # You must set guessed to True if the word is guessed.
        # Things to be looking for:
        #  - Did the user already guess this guess?
        if guesses.count(guess) == 1:
            print("You have already guessed {}, please make another guess.".format(guess))
        else:
        #  - Is the user guessing the whole word?
            if len(guess) == n:
                guesses.append(guess)
            #     - If so, is it correct?
                if guess == word:
                    guessed = True
            #  - Is the user guessing a single letter?
            elif len(guess) == 1:
                guesses.append(guess)
            #     - If so, you'll need your check() function.
                if(check(word, guesses).count("*") == 0):
                    print("Word found! - {}".format(word))
                    guessed = True
            #  - Is the user's guess invalid (the wrong length)?
            else:
                print("Please guess the whole {} letter word, or a single letter.".format(n))
        #
        # Also, don't forget to keep track of the valid guesses.
        print("Guesses so far: {}\n".format(guesses))

    print('{} is it! It took {} tries.'.format(word, len(guesses)))

main()