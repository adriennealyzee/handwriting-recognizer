from flask import Flask, render_template, jsonify, request
import performRecognition
import atexit
from apscheduler.scheduler import Scheduler
import datetime
import logging
logging.basicConfig()
import os

app = Flask(__name__)
cron = Scheduler(daemon=True)
cron.start() # Explicitly kick off the background thread

displaystring = "DISPLAYSTRING222"

@cron.interval_schedule(seconds=1)
def job_function():
    print "inside job function"
    global displaystring
    imgfile = performRecognition.pullLatestFile("maxmspimages")

    imgpath = "maxmspimages/" + imgfile
    print "imgpath", imgpath
    displayint = performRecognition.performRecognitionFn(imgpath)
    # displaystring = "Welcome! x " + displayint
    displaystring = displayint

    # displaystring = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # for i in range(0,5):
        
        # displaystring = i
    print "job fn displaystring ", displaystring

# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))

@app.route('/_stuff', methods= ['GET'])
def stuff():
    global displaystring
    print "inside /_stuff displaystring", displaystring
    # print "inside stuff"
    # imgnum = displaystring
    # print imgnum
    # return jsonify(imgnum=imgnum)
    return jsonify(imgnum=displaystring)

# @app.before_request
# def before_request():
#     if request.path != '/':
#         if request.headers['content-type'].find('application/json'):
#             return 'Unsupported Media Type', 415

@app.route("/")
def main():
    global displaystring
    # imgfile = "adrienne4.jpg"
    print "inside main"
    #while listening:
        # find latest image in 'maxmspimages'
    return render_template('index.html')
    # return displaystring

# @app.route('/echo/', methods=['GET'])
# def echo():
#     global displaystring
#     # ret_data = {"value": request.args.get('echoValue')}
#     ret_data = {"value": displaystring}
#     return jsonify(ret_data)
    
if __name__ == "__main__":
    app.run()