from flask import Flask, render_template
import performRecognition
import atexit
from apscheduler.scheduler import Scheduler
import datetime

app = Flask(__name__)
cron = Scheduler(daemon=True)
cron.start() # Explicitly kick off the background thread

displaystring = "xxxx"

@cron.interval_schedule(seconds=1)
def job_function():
    # imgfile = performRecognition.pullLatestFile("maxmspimages")
    # displayint = performRecognition.performRecognitionFn(imgfile)
    # displaystring = "Welcome! x " + displayint

    displaystring = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # print displaystring

# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))

@app.route('/_stuff', methods= ['GET'])
def stuff():
    print "inside stuff"
    imgnum = displaystring
    print imgnum
    return jsonify(imgnum=5)

@app.route("/")
def main():
    # imgfile = "adrienne4.jpg"

    #while listening:
        # find latest image in 'maxmspimages'
    return render_template('index.html')
    # return displaystring
    
if __name__ == "__main__":
    app.run()