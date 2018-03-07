sudo modprobe bcm2835-v4l2
sudo service motion start
export FLASK_APP=my.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=5000
