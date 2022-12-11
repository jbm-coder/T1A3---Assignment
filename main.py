from stdiomask import getpass
import hashlib
import os
clear = lambda: os.system('clear')
from database import happy
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
    if userAlreadyExist(userName):
        displayUserAlreadyExistMessage()
    else:
        while True:
            userPassword = getpass("Enter Your Password: ")
            if userPassword != '':
                break
        while True:
            confirmPassword = getpass("Confirm Your Password: ")
            if confirmPassword == userPassword:
                break
            else:
                print("Passwords Don't Match")
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
        ask()

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
        print(userName)
        if userAlreadyExist(userName):
            print("You Are Not Registered, Type Q to Return To Main Page")
            print()
        else:
            break
    while True:
        userPassword = getpass("Enter Your Password: ")
        if userAlreadyExist(userName, userPassword):
            print("Incorrect Password")
            print()
        else:
            break
    print()
    print("Logged In!")

    ask()
    

def checkQuit(userName):
    if userName == "q":
        print("You have chose Quit, Returning back to Main Menu")
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
                #print(userName)
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
    print(userName)
    return userName

def hashPassword(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def checkPasswordHash(password, hash):
    return hashPassword(password) == hash

###

def ask():
    initialQuestion = input("How are you today?\nChoose from the following: Happy, Sad, Angry, Depressed, Anxious\nPlease enter how your are feeling: ")
    sanitizeVariable = initialQuestion.lower().strip()
    lastEntry = []
    lastEntry.append(initialQuestion)
    print(lastEntry)

    if sanitizeVariable == "happy":
        quote = random.choice(happy)
        print("\nThat is great! Here is a positive affirmation for you:")
        print(Style.BRIGHT + Back.YELLOW + Fore.GREEN + f"{quote}")
        print("Have a great day!\n")
    else:
        print(Style.BRIGHT + Back.YELLOW + Fore.RED + "**Invalid Entry**")
        print(Style.BRIGHT + Back.YELLOW + Fore.RED + "Please enter a valid response.")
        ask()




    


main()