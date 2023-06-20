# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code; otherwise, the
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

#Defining all functions below for clarity
def reg_user():
    '''Add a new user to the user.txt file'''
    new_username = input("New Username: ")
    
    # Check if the username already exists
    if new_username in username_password:
        print("Username already exists. Please choose a different username.")
        return
   
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "a") as out_file:
            out_file.write(f"\n{new_username};{new_password}")
    else:
        print("Passwords do not match")


def add_task():
    '''Allow a user to add a new task to the tasks.txt file.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the specified format")

    curr_date = date.today()

    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def view_all():
    '''Reads the tasks from tasks.txt file and prints them to the console.'''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


#Updated View Mine with all new requests
def view_mine():
    '''Reads the tasks from tasks.txt file and allows the user to interact with their tasks.'''
    task_count = len(task_list)

#Checking tasks assigned to user and looping for each task to be displayed    
    if task_count == 0:
        print("There are currently no tasks assigned")
        return
    
    print("Tasks assigned to you:")
    for i, task in enumerate(task_list):
        if task['username'] == curr_user:
            print(f"{i+1}. {task['title']}")
        else:
            print("Your username does not have any tasks assigned to it")
    task_choice = input("Enter the number of the task to select it, or enter '-1' to return to the main menu: ")
    
    if task_choice == "-1":
        return
    
    try:
        task_index = int(task_choice) - 1
        selected_task = task_list[task_index]
        
        print(f"\nTask: \t\t {selected_task['title']}")
        print(f"Assigned to: \t {selected_task['username']}")
        print(f"Date Assigned: \t {selected_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Due Date: \t {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Task Description: \n{selected_task['description']}")
        
        if selected_task['completed']:
            print("Status: Completed")
        else:
            print("Status: Not Completed")
        
        edit_choice = input("\nEnter 'c' to mark the task as complete, 'e' to edit the task, or any other key to go back: ")

#Following includes process for editing or marking task as completed  
        if edit_choice.lower() == 'c':
            if selected_task['completed']:
                print("This task is already marked as completed.")
            else:
                selected_task['completed'] = True
                with open("tasks.txt", "w") as task_file:
                    task_list_to_write = []
                    for t in task_list:
                        str_attrs = [
                            t['username'],
                            t['title'],
                            t['description'],
                            t['due_date'].strftime(DATETIME_STRING_FORMAT),
                            t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                            "Yes" if t['completed'] else "No"
                        ]
                        task_list_to_write.append(";".join(str_attrs))
                    task_file.write("\n".join(task_list_to_write))
                print("Task marked as completed.")
        
        elif edit_choice.lower() == 'e':
            if selected_task['completed']:
                print("This task is already marked as completed. Editing is not allowed.")
            else:
                new_username = input("Enter the new username for the task: ")
                new_due_date = input("Enter the new due date for the task (YYYY-MM-DD): ")
                try:
                    due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                    selected_task['username'] = new_username
                    selected_task['due_date'] = due_date_time
                    
                    with open("tasks.txt", "w") as task_file:
                        task_list_to_write = []
                        for t in task_list:
                            str_attrs = [
                                t['username'],
                                t['title'],
                                t['description'],
                                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                "Yes" if t['completed'] else "No"
                            ]
                            task_list_to_write.append(";".join(str_attrs))
                        task_file.write("\n".join(task_list_to_write))
                    print("Task edited successfully.")
                    
                except ValueError:
                    print("Invalid datetime format. Task edit failed.")
        
    except ValueError:
        print("Invalid task number. Returning to the main menu.")

def generate_report():
    # Task Overview Report
    total_tasks = len(task_list)
    completed_tasks = sum(task['completed'] for task in task_list)
    uncompleted_tasks = total_tasks - completed_tasks
    current_date = date.today()
    overdue_tasks = sum(task['due_date'].date() < current_date and not task['completed'] for task in task_list)
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100
    overdue_percentage = (overdue_tasks / total_tasks) * 100

    task_report = f"Task Overview Report\n" \
                  f"---------------------\n" \
                  f"Total tasks: {total_tasks}\n" \
                  f"Completed tasks: {completed_tasks}\n" \
                  f"Uncompleted tasks: {uncompleted_tasks}\n" \
                  f"Overdue tasks: {overdue_tasks}\n" \
                  f"Incomplete percentage: {incomplete_percentage:.2f}%\n" \
                  f"Overdue percentage: {overdue_percentage:.2f}%\n"

    # User Overview Report
    total_users = len(username_password)
    user_report = f"\nUser Overview Report\n" \
                  f"---------------------\n" \
                  f"Total users: {total_users}\n"

    for user in username_password:
        user_tasks = sum(task['username'] == user for task in task_list)
        user_completed_tasks = sum(task['username'] == user and task['completed'] for task in task_list)
        user_incomplete_tasks = sum(task['username'] == user and not task['completed'] for task in task_list)
        user_overdue_tasks = sum(task['username'] == user and not task['completed'] and task['due_date'].date() < current_date for task in task_list)
        user_percentage = (user_tasks / total_tasks) * 100
        user_completed_percentage = (user_completed_tasks / user_tasks) * 100
        user_incomplete_percentage = (user_incomplete_tasks / user_tasks) * 100
        user_overdue_percentage = (user_overdue_tasks / user_tasks) * 100

        user_report += f"\nUser: {user}\n" \
                       f"Total tasks assigned: {user_tasks}\n" \
                       f"Percentage of total tasks: {user_percentage:.2f}%\n" \
                       f"Percentage of completed tasks: {user_completed_percentage:.2f}%\n" \
                       f"Percentage of incomplete tasks: {user_incomplete_percentage:.2f}%\n" \
                       f"Percentage of overdue tasks: {user_overdue_percentage:.2f}%\n"

    # Write reports to files
    with open("task_overview.txt", "w") as task_file:
        task_file.write(task_report)

    with open("user_overview.txt", "w") as user_file:
        user_file.write(user_report)

    print("Reports have been created to task_overview.txt and user_overview.txt")



while True:
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate Report
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr':
        generate_report()
#Specific instance for ds, now with reading text files
    elif menu == 'ds' and curr_user == 'admin':
        num_users = len(username_password.keys())
        num_tasks = len(task_list)
        if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
            generate_report()

# Read and display the task overview report
        with open("task_overview.txt", "r") as task_file:
            task_report = task_file.read()
        print("Task Overview Report:")
        print(task_report)

# Read and display the user overview report
        with open("user_overview.txt", "r") as user_file:
            user_report = user_file.read()
        print("User Overview Report:")
        print(user_report)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice. Please try again")
