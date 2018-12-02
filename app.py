from flask import Flask
from flask import Response, render_template, send_file, jsonify, abort, request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image
import io
import cv2
from skimage.io import imsave
from camera import VideoCamera
import random
from pymongo import MongoClient
import time
from datetime import datetime, date, time, timedelta
from collections import defaultdict

app = Flask(__name__)
mongoClient = MongoClient('mongodb://localhost:27017/')
storeName = 'TestStore'
storeLocation = 'Bellevue_98004'
storeDatabase = mongoClient[storeName]
storeCollection = storeDatabase[storeLocation]


@app.route('/head_turns_last_day')
def head_turns_last_day():
    results = storeCollection.find()
    timestampHourBack = (datetime.utcnow() - timedelta(hours=24)).timestamp() * 1000
    faces = set()

    for result in results:
        timestamp = result['Timestamp']
        if timestamp > timestampHourBack:
            if 'Face' in result['Person']:
                faces.add(result['Person']['Index'])

    return str(len(faces))


@app.route('/foot_traffic_last_day')
def foot_traffic_last_day():
    results = storeCollection.find()
    timestampHourBack = (datetime.utcnow() - timedelta(hours=24)).timestamp() * 1000
    persons = set()

    for result in results:
        timestamp = result['Timestamp']
        if timestamp > timestampHourBack:
            persons.add(result['Person']['Index'])

    return str(len(persons))

@app.route('/analytics')
def analytics():
    startTimestamp = int(request.args.get('start'))
    results = storeCollection.find()
    timestamp_face_count_dict, timestamp_person_count_dict, timestamp_male_count_dict, timestamp_female_count_dict, timestamp_youth_count_dict, timestamp_adult_count_dict, timestamp_seniors_count_dict, timestamp_happy_count_dict, timestamp_calm_count_dict, timestamp_disgusted_count_dict,timestamp_confused_count_dict, timestamp_surprised_count_dict, timestamp_sad_count_dict, timestamp_angry_count_dict  = [defaultdict(int)] * 14

    for result in results:
        timestamp = result['Timestamp']
        if timestamp > startTimestamp:
            timestamp_person_count_dict[timestamp] += 1

            if 'Face' in result['Person']:
                timestamp_face_count_dict[timestamp] += 1

                # Male count
                if result['Person']['Face']['Gender']['Value'] == 'Male' and result['Person']['Face']['Gender']['Confidence'] >= 75:
                    timestamp_male_count_dict[timestamp] += 1
                
                # Female count
                if result['Person']['Face']['Gender']['Value'] == 'Female' and result['Person']['Face']['Gender']['Confidence'] >= 75:
                    timestamp_female_count_dict[timestamp] += 1 
                    
                
                avg_age = (result['Person']['Face']['AgeRange']['Low'] + result['Person']['Face']['AgeRange']['High']) / 2
                
                # Youth count
                if avg_age >= 0 and avg_age < 18:
                    timestamp_youth_count_dict[timestamp] += 1 
                # Adult count
                elif avg_age >= 18 and avg_age < 60:
                    timestamp_adult_count_dict[timestamp] += 1
                # Seniors count
                else:
                    timestamp_seniors_count_dict[timestamp] += 1 
                    
                # most likely mood count
                most_likely_mood = max(result['Person']['Face']['Emotions'], key=lambda x:x['Confidence'])['Type']
                if most_likely_mood == 'HAPPY':
                    timestamp_happy_count_dict[timestamp] += 1
                elif most_likely_mood == 'CALM':
                    timestamp_calm_count_dict[timestamp] += 1
                elif most_likely_mood == 'DISGUSTED':
                    timestamp_disgusted_count_dict[timestamp] += 1
                elif most_likely_mood == 'CONFUSED':
                    timestamp_confused_count_dict[timestamp] += 1
                elif most_likely_mood == 'SURPRISED':
                    timestamp_surprised_count_dict[timestamp] += 1
                elif most_likely_mood == 'SAD':
                    timestamp_sad_count_dict[timestamp] += 1
                else:
                    timestamp_angry_count_dict[timestamp] += 1
                    
            else:
                timestamp_face_count_dict[timestamp], timestamp_person_count_dict[timestamp], timestamp_male_count_dict[timestamp], timestamp_female_count_dict[timestamp], timestamp_youth_count_dict[timestamp], timestamp_adult_count_dict[timestamp], timestamp_seniors_count_dict[timestamp], timestamp_happy_count_dict[timestamp], timestamp_calm_count_dict[timestamp], timestamp_disgusted_count_dict[timestamp],timestamp_confused_count_dict[timestamp], timestamp_surprised_count_dict[timestamp], timestamp_sad_count_dict[timestamp], timestamp_angry_count_dict[timestamp]  = [0] * 14

    count_dicts = [timestamp_face_count_dict, timestamp_person_count_dict, timestamp_male_count_dict, timestamp_female_count_dict, timestamp_youth_count_dict, timestamp_adult_count_dict, timestamp_seniors_count_dict, timestamp_happy_count_dict, timestamp_calm_count_dict, timestamp_disgusted_count_dict,timestamp_confused_count_dict, timestamp_surprised_count_dict, timestamp_sad_count_dict, timestamp_angry_count_dict]

    return count_dicts

@app.route('/')
def index():
    return render_template(
        'dashboard.html',
        foot_traffic=int(foot_traffic_last_day()),
        head_turns=head_turns_last_day())

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/icons')
def icons():
    return render_template('icons.html')

@app.route('/typography')
def typography():
    return render_template('typography.html')

@app.route('/maps')
def maps():
    return render_template('maps.html')

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

@app.route('/table')
def table():
    return render_template('table.html')

@app.route('/template')
def template():
    return render_template('template.html')

@app.route('/upgrade')
def upgrade():
    return render_template('upgrade.html')

@app.route('/user')
def user():
    return render_template('upgrade.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera('beach_walk.avi')), mimetype='multipart/x-mixed-replace; boundary=frame')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

def mk_graphs(df):
    fig, ax = plt.subplots()
    ax.hist(df['number of people'])
    fig.canvas.draw()

    return fig

def update_graph_helper(df):

    fig, ax = plt.subplots()

    ax.hist(df['number of people'])

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    plt.close('all')

    return output


def dynamic_graph():

    old = new = None
    while True:
        data = pd.read_csv('MOCK_DATA.csv')
        out = update_graph_helper(data).getvalue()
        time.sleep(10)
        print('ok')

        old = new
        new = out

        print(old == new)

        yield out


@app.route('/plot')
def plot():
    #fig = mk_graphs(data)
    #output = io.BytesIO()
    #FigureCanvas(fig).print_png(output)
    temp = dynamic_graph()
    return Response(temp, mimetype='multipart/x-mixed-replace; boundary=frame')





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)