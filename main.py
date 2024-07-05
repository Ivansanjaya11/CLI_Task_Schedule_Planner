import pandas as pd
from PyInquirer import prompt
import signal
import time
import sys
import json

# global data structure for to-do list and study plan
to_do_list = []
study_plan = []
data_file = 'data.json' # file to store data

# signal handler for graceful exit
def signal_handler(sig, frame):
    save_data()
    print('exiting and saving data...')
    time.sleep(2)
    sys.exit(0)

# saving data in json format to data_file
def save_data():
    data = {
        'to_do_list': to_do_list,
        'study_plan': study_plan
    }
    with open(data_file, 'w') as f:
        json.dump(data, f)
    print('data saved.')

# loading and reading data from data_file
# if there is no 'to_do_list' or 'study_plan', create empty list (for initial list creation)
def load_data():
    global to_do_list, study_plan
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
            to_do_list = data.get('to_do_list', [])
            study_plan = data.get('study_plan', [])
        print('data loaded.')
    except FileNotFoundError:
        print('no existing data found. Starting fresh.')

# create main_menu page
# for choosing what the user wants to do (to-do list or study plan)
def main_menu():
    questions = [
        {
            'type': 'list',
            'name': 'main_menu',
            'message': 'Main Menu | Choose what you\'re going to do',
            'choices': [
                'manage to-do list',
                'manage study planner',
                'exit'
            ]
        }
    ]
    while True:
        answer = prompt(questions)
        if answer['main_menu'] == 'manage to-do list':
            manage_to_do_list()
        elif answer['main_menu'] == 'manage study planner':
            manage_study_planner()
        else:
            save_data()
            print('exiting program...')
            time.sleep(2)
            break

###################
### to-do list
###################

def manage_to_do_list():
    questions = [
        {
            'type': 'list',
            'name': 'todo_menu',
            'message': 'To-Do List Menu',
            'choices': [
                'Add task',
                'View tasks',
                'Edit task',
                'Delete task',
                'Back to main menu'
            ]
        }
    ]
    while True:
        answer = prompt(questions)
        if answer['todo_menu'] == 'Add task':
            add_task()
        elif answer['todo_menu'] == 'View tasks':
            view_task()
        elif answer['todo_menu'] == 'Edit tasks':
            edit_task()
        elif answer['todo_menu'] == 'Delete task':
            delete_task()
        else:
            break

def view_task():
    if not to_do_list:
        print('no tasks available')
        return
    for idx, task in enumerate(to_do_list, start=1):
        print(f"{idx}. {task}")

def add_task():
    while True:
        question = [
            {
                'type': 'input',
                'name': 'task_input',
                'message': 'Enter task: '
            }
        ]
        answer = prompt(question)
        to_do_list.append(answer['task_input'])
        print(f"Task '{answer['task_input']}' has been added.")

        continue_questions = [
            {
                'type': 'confirm',
                'name': 'continue_add_task',
                'message': 'Do you want to add another task?',
                'default': False
            }
        ]
        continue_answer = prompt(continue_questions)
        if not continue_answer['continue_add_task']:
            break


def edit_task():
    if not to_do_list:
        print('no tasks available.')
        return
    task_choices = [{'name': task} for task in to_do_list]
    questions = [
        {
            'type': 'list',
            'name': 'task_to_edit',
            'message': 'Select task to edit: ',
            'choices': task_choices
        },
        {
            'type': 'input',
            'name': 'new_task_name',
            'message': 'Enter new task name: '
        }
    ]
    answer = prompt(questions)
    task_index = to_do_list.index(answer['task_to_edit'])
    to_do_list[task_index] = answer['new_task_name']
    print(f"task updated to '{answer['new_task_name']}'.")

def delete_task():
    if not to_do_list:
        print('no tasks available.')
        return
    task_choices = [{'name': task} for task in to_do_list]
    questions = [
        {
            'type': 'list',
            'name': 'task_to_delete',
            'message': 'Select task to delete: ',
            'choices': task_choices
        }
    ]
    answer = prompt(questions)
    to_do_list.remove(answer['task_to_delete'])
    print(f"Task '{answer['task_to_delete']}' has been deleted.")


###################
### study planner
###################

def manage_study_planner():
    questions = [
        {
            'type': 'list',
            'name': 'study_plan_menu',
            'message': 'Study Plan Menu',
            'choices': [
                'Schedule study session',
                'View study session',
                'Edit study session',
                'Delete Study session',
                'Back to main menu'
            ]
        }
    ]
    while True:
        answer = prompt(questions)
        if answer['study_plan_menu'] == 'Schedule study session':
            schedule_study_session()
        elif answer['study_plan_menu'] == 'View study session':
            view_study_plan()
        elif answer['study_plan_menu'] == 'Edit study session':
            edit_study_plan()
        elif answer['study_plan_menu'] == 'Delete study session':
            delete_study_session()
        else:
            break

def view_study_plan():
    if not study_plan:
        print('no study session available.')
        return
    schedule = pd.DataFrame(study_plan)
    schedule = schedule.pivot(index='time', columns='day', values='name')
    schedule = schedule.fillna('')
    print(schedule)

def schedule_study_session():
    questions = [
        {
            'type': 'input',
            'name': 'session_day',
            'message': 'Enter session day: '
        },
        {
            'type': 'input',
            'name': 'session_time',
            'message': 'Enter session time: '
        },
        {
            'type': 'input',
            'name': 'session_name',
            'message': 'Enter study session: '
        }
    ]
    answer = prompt(questions)
    study_plan.append(
        {
            'day': answer['session_day'],
            'time': answer['session_time'],
            'name': answer['session_name']
        }
    )
    print(f"Study session '{answer['session_name']}' scheduled on {answer['session_day']} at {answer['session_time']}")

def edit_study_plan():
    if not study_plan:
        print('no study sessions available')
        return
    session_choices = [
        {
            'name': f"{session['name']} ({session['day']} at {session['time']})",
            'value': session
        }
        for session in study_plan
    ]
    questions = [
        {
            'type': 'list',
            'name': 'session_to_edit',
            'message': 'Select study session to edit: ',
            'choices': session_choices
        },
        {
            'type': 'input',
            'name': 'new_session_name',
            'message': 'Enter new session name: '
        },
        {
            'type': 'input',
            'name': 'new_session_day',
            'message': 'Enter new session day: '
        },
        {
            'type': 'input',
            'name': 'new_session_time',
            'message': 'Enter new session time: '
        }
    ]
    answer = prompt(questions)
    session_index = next(
        (idx for idx, session in enumerate(study_plan) if session['name'] == answer['session_to_edit']),
        None
    )
    if session_index is not None:
        study_plan[session_index] == {
            'day': answer['new_session_day'],
            'time': answer['new_session_time'],
            'name': answer['new_session_name']
        }
        print(f"Study session updated to '{answer['new_session_name']}' on {answer['new_session_day']} at {answer['new_session_time']}.")

def delete_study_session():
    if not study_plan:
        print('no study sessions available.')
        return
    while True:
        session_choices = [
            {
                'name': f"{session['name']} ({session['day']} at {session['time']})",
                'value': session
            }
            for session in study_plan
        ]
        questions = [
            {
                'type': 'list',
                'name': 'session_to_delete',
                'message': 'Select study session to delete: ',
                'choices': session_choices
            }
        ]
        answer = prompt(questions)
        session_to_delete = answer['session_to_delete']
        study_plan.remove(session_to_delete)
        print(f"Study session '{session_to_delete['name']}' on {session_to_delete['day']} at {session_to_delete['time']}' has been deleted.")

        continue_questions = [
            {
                'type': 'confirm',
                'name': 'continue_delete',
                'message': 'Do you want to delete another session?',
                'default': False
            }
        ]
        continue_answer = prompt(continue_questions)
        if not continue_answer['continue_delete']:
            break

def main():
    load_data() # load existing data from storage
    signal.signal(signal.SIGINT, signal_handler) # register signal handler for graceful exit
    main_menu() # start main menu loop

if __name__ == '__main__':
    main()