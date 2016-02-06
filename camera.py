import cv2
import threading
import datetime

# Camera 0 is the integrated web cam on my netbook
camera_port = 0

# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
camera = cv2.VideoCapture(camera_port)

# Captures a single image from the camera and returns it in PIL format
def get_image():
    global camera
    # read is the easiest way to get a full image out of a VideoCapture object.
    retval, im = camera.read()
    return im

def take_pic(filename):
    print "inside take_pic"
    #Number of frames to throw away while the camera adjusts to light levels
    ramp_frames = 30
    # Ramp the camera - these frames will be discarded and are only used to allow v4l2
    # to adjust light levels, if necessary
    for i in xrange(ramp_frames):
     temp = get_image()
    print("Taking image...")
    # Take the actual image we want to keep
    camera_capture = get_image()
    file = "python_images/" + filename + ".jpg"
    # A nice feature of the imwrite method is that it will automatically choose the
    # correct format based on the file extension you provide. Convenient!
    cv2.imwrite(file, camera_capture)
     
    # You'll want to release the camera, otherwise you won't be able to create a new
    # capture object until your script exits
    
# count = 0 

def camera_timer():
  global count
  threading.Timer(2.0, camera_timer).start()
  # count += 1
  now = datetime.datetime.now()
  seconds = (now-datetime.datetime(1970,1,1)).total_seconds()
  filename = str(int(seconds))
  # take_pic(str(count))
  take_pic(filename)

if __name__ == "__main__":

    # del(camera)
    
    camera_timer()

