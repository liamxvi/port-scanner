import pyfiglet
from pyfiglet import Figlet
from colorama import Fore, Back, Style
from time import sleep
from progress.bar import Bar
import datetime
import socket
import sys
import os
import argparse
import time

def scanPorts(host, start_port, end_port):
    try:
        # translate hostname to IP address
        host_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"Error resolving hostname: {host}")
        sys.exit()

    # set up progress bar
    bar = Bar('Scanning', max=end_port - start_port + 1)

    openPorts = []
    # iterate over the specified port range
    for port in range(start_port, end_port+1):
        try:
            # create a new socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # set timeout to 1 second
            #s.settimeout(10)
            # try connecting to the host and port
            result = s.connect_ex((host_ip, port))
            if result == 0:
                openPorts.append(port)
            s.close()
        except socket.timeout:
            # if a timeout occurs, print an error message
            print(f"Timeout occurred while scanning port {port}")
        except Exception as e:
            print(f"An error occurred while scanning port {port}: {e}")

                # update progress bar
        bar.next()

    # finish progress bar
    bar.finish()
    for openPort in openPorts:
        print(f"Port {openPort} is open")#
    time.sleep(1)
    return openPorts

def mainMenu():
    print(Fore.RED + "-" * 80)
    ascii_banner = pyfiglet.figlet_format("Port Scanner v1.0")
    print(Fore.RED + ascii_banner)
    print("-" * 80)
    print(Fore.LIGHTBLACK_EX + "1. Scan ports")
    print(Fore.LIGHTBLACK_EX + "2. View previous scans")
    print(Fore.LIGHTBLACK_EX + "3. Quit")
    choice = input("Input your choice: ")
    while choice not in ["1", "2", "3"]:
        print("Invalid choice. Please enter 1, 2, or 3.")
        choice = input("Input your choice: ")
    return choice

#prints a simple menu for the user to select from options between 1 - 3. There is various bits of code which is for purely cosmetic purposes.

def save_scan_to_file(host, start_port, end_port, scan_results):
    option = input("Would you like to save the results? Y/N ")
    if option.lower() == 'y':
        try:
            with open(f"{host}_{start_port}_{end_port}.txt", "w") as f:
                for port in scan_results:
                    f.write(f"Port {port} is Open\n")
                print("File saved successfully")
        except:
            print("Error saving scan results to file")
    

#saves the scan results to a file with a name in the format host_start_port_end_port.txt. The file will be created in the same directory as the script that is running.

def viewScanHistory():
    files = [f for f in os.listdir() if f.endswith(".txt")]
    if not files:
        print("No scan history found.")
        return

    print("Scan history:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}") 

    while True:
        choice = input("Enter the number of the scan you want to view (or enter 'q' to quit): ")
        if choice == 'q':
            return
        try:
            choice = int(choice)
            if choice < 1 or choice > len(files):
                print(f"Invalid choice. Enter a number between 1 and {len(files)} (or enter 'q' to quit).")
                continue
            with open(files[choice - 1], "r") as f:
                print(f.read())
        except ValueError:
            print("Invalid choice. Enter a number (or enter 'q' to quit).")

#checks if any scan history files were found. If none were found, it prints a message and returns. 
#If files are found, it loops until the user enters a valid choice or 'q' to quit. It also checks that the user's input is a valid integer between 1 and the number of files. 
#If the input is not valid, it prints an error message and loops again.

if __name__ == "__main__":
    host = "" #this indicates that the host will be the user selection
    start_port = 1 #this will be the starting port of which the user may select 
    end_port = 65535 #this will be the finish port of which the user may select
    if len(sys.argv) >= 2: 
        host = sys.argv[1]
        if len(sys.argv) == 4:
            start_port = int(sys.argv[2])
            end_port = int(sys.argv[3])
    while True:
        choice = mainMenu()
        if choice == "1": #if the user selects 1 on the main menu then it will carry onto the selection of a desired host ip address
            if host == "": #this will promot the user to input the host target address 
                host = input(Fore.LIGHTBLACK_EX + "Enter the host name or IP address: ") #this will ask the user to input a desired host name or ip address 
            start_port = int(input(Fore.LIGHTBLACK_EX + "Enter the starting port: ")) #prompts the user to select a starting port
            end_port = int(input(Fore.LIGHTBLACK_EX + "Enter the ending port: ")) #promts the user to select an end port 
            openPorts = scanPorts(host, int(start_port), int(end_port)) #this will scan all of the ports between the starting port and the ending port 
            save_scan_to_file(host, start_port, end_port, openPorts)
        elif choice == "2":
            viewScanHistory() #if the user selects option 2 then it will rtun the scan history function
        elif choice == "3":
            print("Goodbye!") #if the user selects option 3 then the output will print a message saying goodbye 
            sys.exit() #the system will then exit the python application 
        else:
            print(Fore.RED + "Invalid choice. Try again.") #if any other option other than the required options are selected then it will promot the user to try another selection