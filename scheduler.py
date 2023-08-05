from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from scraperModule import StudyRoomBooker
from minheap import taskObj, taskMinHeap
import webbrowser
import logging, signal, os
import csv

app = Flask(__name__)
class StudyRoomScheduler:
    def __init__(self, booker):
        self.mainBrowser = booker # <-- class creates the driver in the init
        self.username = ""
        self.password = "password"
        self.ucfID = ""
        self.taskHeap = taskMinHeap()
        self.taskQueue = []

    def write_to_csv(self):
        try:
            with open("data.txt", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([f'{self.username}', f'{self.ucfID}'])
                writer.writerow(['Jobs:'])
                writer.writerow(['date', 'start_time', 'duration', 'reservationType', 'room_option', 'room_number', 'min_capacity'])
                while not self.taskHeap.isEmpty():
                    writer.writerow(self.taskHeap.extractMin().get_all_variables())
        except Exception as e:
            logging.error(f"Failed to dump data to txt: {e}")

    def save_data_on_shutdown(self):
        self.mainBrowser.close()
        self.write_to_csv()

    def schedule_Task(self, username, password, ucfID, date, start_time, duration, reservationType, room_option, room_number, min_capacity):
        input_date = datetime.strptime(date, '%Y-%m-%d')
        current_date = datetime.now()
        date_difference = input_date - current_date
        if date_difference >= timedelta(days=7):
            newTask = taskObj(date, start_time, duration, reservationType, room_option, room_number, min_capacity)
            self.taskHeap.insert(newTask)
        else:
            if reservationType == "group":
                room_number = self.mainBrowser.rand_room(room_option, min_capacity)
            try:
                self.mainBrowser.book_room(username, password, ucfID, date, room_number, start_time, duration)
            except Exception as e:
                # Log the error
                logging.exception("An error occurred while scheduling the task: %s", str(e))
    
    #Only to be called within enqueue task
    def valid_task(self):
        self.username = request.form.get('input1')
        self.password = request.form.get('input2')
        start_time = request.form.get('input4')
        duration = request.form.get('input5')
        reservationType = request.form.get('input6')
        room_number = request.form.get('input7')
        room_option = request.form.get('room-option')
        min_capacity = request.form.get('input8')
        self.ucfID = request.form.get('input9')
        date = request.form.get('input3')

        #while the below is in progress I want to have a loading screen of sorts
        #print(self.mainBrowser.driver.session_id)
        if self.schedule_Task(self.username, self.password, self.ucfID, date, start_time, duration, reservationType, room_option, room_number, min_capacity):
            return redirect(url_for('completion_screen'))
        return render_template('tester.html', username=self.username, password=self.password, start_time=start_time,
                                duration=duration,reservation_type=reservationType, min_capacity=min_capacity,
                                 date=date, room_option=room_option, room_number=room_number,ucfID = self.ucfID)

    def process_file(self):
        tasks =[]
        try:
            with open('data.txt', 'r') as file:
                reader = csv.reader(file)
                self.username, self.ucfID = next(reader)
                next(reader)
                next(reader)
                for row in reader:
                    if len(row) == 7:
                        tasks.append(row)  
            for task in tasks:
                date, start_time, duration, reservationType, room_option, room_number, min_capacity = task
                current_date = datetime.now()
                date_difference = datetime.strptime(date, '%Y-%m-%d') - current_date
                if date_difference >= timedelta(days=7):
                    newTask = taskObj(date, start_time, duration, reservationType, room_option, room_number, min_capacity)
                    self.taskHeap.insert(newTask)
                elif date_difference > 0: #check for past
                    self.taskQueue.append(task)
                    self.schedule_Task(self.username, self.password, self.ucfID, date, start_time, duration, reservationType, room_option, room_number, min_capacity)
                else:
                    logging.info(f"Previously Scheduled Task: {task} is invalid")

        except Exception as e:
            logging.error("An error occurred while processing the file: %s", str(e))

scheduler = StudyRoomScheduler(booker=StudyRoomBooker())

def keyboard_interrupt_handler(signal, frame):
    logging.info(f'Keyboard Interrupt (Ctrl + C) detected. Exiting now, this may take a minute...')
    scheduler.mainBrowser.close()
    os._exit(0)

#ROUTES
@app.route('/task_enqueue', methods=['POST'])
def enqueue_task():
    return scheduler.valid_task()

@app.route('/completion')
def completion_screen():
    # Render the completion template
    return render_template('completion.html')

@app.route('/')
def index():
    return render_template('index.html',username = scheduler.username, password = scheduler.password, ucfID = scheduler.ucfID)

@app.route('/shutdown', methods=['POST'])
def shutdown_server():
    if request.method == 'POST':
        scheduler.save_data_on_shutdown()
        logging.info("Server Shutdown")
        os._exit(0)
    return "Server shutting down..."
    
if __name__ == '__main__':
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)
    logging.basicConfig(filename='app.log', level=logging.INFO,filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('werkzeug')
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    
    scheduler.process_file()
    host = '127.0.0.1'  
    port = 5000  
    url = f'http://{host}:{port}/'
    webbrowser.open(url) 
    app.run(host=host, port=port, debug=False, use_reloader=False)
    
