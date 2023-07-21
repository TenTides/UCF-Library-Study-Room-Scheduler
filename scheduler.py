from flask import Flask, render_template, request
from celery import Celery
import datetime
import csv

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


username = ""
password = ""
tasks = []

# def load_tasks():
#     with open('tasks.txt', 'r') as file:
#         for line in file:
#             task_data = line.strip().split(',')
#             task_name = task_data[0]
#             task_schedule = datetime.datetime.strptime(task_data[1], '%Y-%m-%d %H:%M:%S')
#             task_data = task_data[2]
#             schedule_task.apply_async(args=[task_name, task_data], eta=task_schedule)

# @celery.task
# def schedule_task(task_name, task_data):
#     # Your task code here
#     print(f"Executing task '{task_name}' with data: {task_data}")
@app.route('/task_enqueue', methods=['POST'])
def valid_task():
    username = request.form.get('input1')
    password = request.form.get('input2')
    date = request.form.get('input3')
    start_time = request.form.get('input4')
    duration = request.form.get('input5')
    reservationType = request.form.get('input6') 
    min_capacity = request.form.get('input7')
    room_option = request.form.get('room-option')
    min_capacity = request.form.get('input8')

    return render_template('tester.html', username=username,password=password, start_time=start_time,
                            duration=duration,reservation_type=reservationType, min_capacity=min_capacity,
                            date=date, room_option=room_option)

def process_file():
    global username,password,tasks
    with open('data.txt', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                if row[0] == 'Jobs:':
                    break  # Stop reading when tasks section is encountered
                username, password = row
                # Process username and password 
            if len(row) == 4:
                tasks.append(row)  # Store the task data
    # Pass the tasks to Celery or perform any other required operations
    for task in tasks:
        time_task_was_queued, desired_schedule_date, time_of_reservation, duration_of_stay = task
        # Process task (e.g., schedule the task with Celery)

@app.route('/')
def index():
    process_file()
    # Schedule the task and save it to the file
    #task_name = 'task3'
    # task_schedule = datetime.datetime.now() + datetime.timedelta(seconds=10)
    # task_data = 'task3_data'
    # with open('tasks.txt', 'a') as file:
    #     file.write(f"{task_name},{task_schedule.strftime('%Y-%m-%d %H:%M:%S')},{task_data}\n")
    # schedule_task.apply_async(args=[task_name, task_data], eta=task_schedule)

    return render_template('index.html',username = username, password = password)

if __name__ == '__main__':
    # load_tasks()  # Load tasks from the file on Flask server startup
    app.run(debug=True)