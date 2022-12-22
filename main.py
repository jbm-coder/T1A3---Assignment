from stdiomask import getpass
import hashlib
import os
clear = lambda: os.system('clear')
from database import happy, sad, angry, depressed, anxious
import random
import time
from cfonts import render
from colorama import init, Fore, Back, Style
init(autoreset=True)

output = render('Friendster', colors=['green', 'yellow'], align='center')
print(output)
time.sleep(2)

def main():
    clear()
    print("MAIN MENU")
    print("---------")
    print()
    print("1 - Register")
    print("2 - Login")
    print()
    while True:
        print()
        userChoice = input("Choose An Option: ")
        if userChoice in ['1', '2']:
            break
    if userChoice == '1':
        register()
    else:
        Login()

def register():
    clear()
    print("REGISTER")
    print("--------")
    print()
    while True:
        userName = input("Enter Your Name: ").title()
        if userName != '':
            break
    userName = sanitizeName(userName)

    checkQuit(userName)

    if userAlreadyExist(userName):
        displayUserAlreadyExistMessage()
    else:
        while True:
            userPassword = getpass("Enter Your Password: ")
            if userPassword != '':
                break
        while True:
            confirmPassword = getpass("Confirm Your Password: ")
            checkQuitPassword(confirmPassword)
            if confirmPassword == userPassword:
                break
            else:
                print("Incorrect - Retype your password or enter Q to quit")
                print()
        if userAlreadyExist(userName, userPassword):
            while True:
                print()
                error = input("You Are Already Registered.\n\nPress (T) To Try Again:\nPress (L) To Login: ").lower()
                if error == 't':
                    register()
                    break
                elif error == 'l':
                    Login()
                    break
        addUserInfo([userName, hashPassword(userPassword)])

        print()
        print("Registered!")
        user_mood = read_file() # get the previous mood data of all the users
        mood = ask() # ask for the user's mood
        user_mood[userName] = ["1", mood] # add this user's name and mood to the dictionary
        write_file(user_mood) # write the data to the file

def Login():
    clear()
    print("LOGIN")
    print("-----")
    print()
    usersInfo = {}
    with open('userInfo.txt', 'r') as file:
        for line in file:
            line = line.split()
            usersInfo[line[0]] = line[1]
    while True:
        userName = input("Enter Your Name: ").title()
        userName = sanitizeName(userName)
        checkQuit(userName)
        if not userAlreadyExist(userName):
            print("You Are Not Registered, Type Q to Return To Main Page")
            print()
        else:
            break
    while True:
        userPassword = getpass("Enter Your Password: ")
        checkQuitPassword(userPassword)
        if not userAlreadyExist(userName, userPassword):
            print("Incorrect - Retype your password or enter Q to quit")
            print()
        else:
            break
    print()
    print("Logged In!")

    user_mood = read_file() # read and get the previous mood data of all the users

    app_used = 0 # variable to keep record of how many times user used our application
    mood_lst = [] # initializing the list to keep track of the current user's mood

    # if the user data is in our dictionary
    if userName in user_mood:
        data = user_mood[userName] # ['5', 'happy', 'sad', 'angry', 'happy', 'happy'] get user data
        app_used = int(data[0]) # get the numbers of tieme user used our data
        mood_lst = user_mood[userName] # get the list of mood for this user

        #if the pplication has been used more than 10 times, we reset all the data
        if app_used >= 10:
            print("Congrats you used our application 10 times")
            app_used = 0
            mood_lst = []
        print(f"Hello {userName}, the last time you used our application you were feeling {data[-1]} ")

    mood = ask()

    count_mood = {} # dictionary to store the mood stats of this specific user

    # if the application has been used 10 times, we calculate the stats
    if app_used + 1 >= 10:
        print("Congrats you used our application 10 times")
        for prev_mood in user_mood[userName][1:]:
            if prev_mood in count_mood:
                count_mood[prev_mood] += 1
            else:
                count_mood[prev_mood] = 1
        if mood in count_mood:
            count_mood[mood] += 1
        else:
            count_mood[mood] = 1
        
        print("\nHere are the stats of your 10 entries:\n")
        for myMood in count_mood:
            print(f"{myMood}: {count_mood[myMood]}")


    if len(mood_lst) == 0:
        user_mood[userName] = mood_lst
        user_mood[userName].append(str(app_used + 1))
    else:
        user_mood[userName][0] = str(app_used + 1)
    user_mood[userName].append(mood)

    write_file(user_mood)



def checkQuit(userName):
    if userName == "q":
        print("You have chose Quit, Returning back to Main Menu")
        time.sleep(2)
        main()

def checkQuitPassword(userPassword):
    if userPassword == "q":
        print("You have chose to Quit, Returning back to Main Menu")
        time.sleep(2)
        main()

def checkConfirmedPassword(confirmedPassword):
    if confirmedPassword == "q":
        print("You have chose to Quit, Returning back to Main Menu")
        time.sleep(2)
        main()

def addUserInfo(userInfo: list):
    with open('userInfo.txt', 'a') as file:
        for info in userInfo:
            file.write(info)
            file.write(' ')
        file.write('\n')

def userAlreadyExist(userName, userPassword=None):
    if userPassword == None:
        with open('userInfo.txt', 'r') as file:
            for line in file:
                line = line.split()
                if line[0] == userName:
                    return True
        return False
    else:
        userPassword = hashPassword(userPassword)
        usersInfo = {}
        with open('userInfo.txt', 'r') as file:
            for line in file:
                line = line.split()
                if line[0] == userName and line[1] == userPassword:
                    usersInfo.update({line[0]: line[1]})
        if usersInfo == {}:
            return False
        return usersInfo[userName] == userPassword

def displayUserAlreadyExistMessage():
    while True:
        print()
        error = input("You Are Already Registered.\n\nPress (T) To Try Again:\nPress (L) To Login: ").lower()
        if error == 't':
            register()
            break
        elif error == 'l':
            Login()
            break

def sanitizeName(userName):
    userName = userName.lower().split()
    userName = ''.join(userName)
    return userName

def hashPassword(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def checkPasswordHash(password, hash):
    return hashPassword(password) == hash



def ask():
    initialQuestion = input("How are you today?\nChoose from the following: Happy, Sad, Angry, Depressed, Anxious\nPlease enter how your are feeling: ")
    sanitizeVariable = initialQuestion.lower().strip()

    if sanitizeVariable == happy or sad or angry or depressed or anxious:
        quote = random.choice(happy or sad or angry or depressed or anxious)
        print("\nThank you for your entry. Here is a positive affirmation for you:")
        print(Style.BRIGHT + Back.YELLOW + Fore.GREEN + f"{quote}")
        print("Have a great day!\n")
        return sanitizeVariable

    else:
        print(Style.BRIGHT + Back.YELLOW + Fore.RED + "**Invalid Entry**")
        print(Style.BRIGHT + Back.YELLOW + Fore.RED + "Please enter a valid response.")
        ask()

def write_file(user_mood):
    """function to write the user mood data back to the file"""

    file = open('usermood.txt', 'w') # open text file in write mode

    # iterate through each value in our dictionary
    for user in user_mood:
        file.write(user + " " + " ". join(user_mood[user]) + "\n") # write the data in specific format

    file.close()


def read_file():
    """function to read the previous mood of all the users and add them to the dictionary"""

    file = open('usermood.txt', 'r') # open the file in read mode
    user_mood = {} # dictionary to store the user mood for their last entries if any
     # iterate though all the lines in the file
    for line in file:
        temp = line.split() # split the lines on the spacing
        user_mood[temp[0]] = temp[1:] # add the user mood plus their previous entry number in the dictionary
    
    file.close() # close the file
    return user_mood # return the data


main()
