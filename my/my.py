import sqlite3
from flask import Flask,render_template, url_for, request, redirect, session
from time import sleep
import motor
import threading
from my_functions import blink, distance_detected

tdist=[]
app=Flask(__name__)
conn = sqlite3.connect(':memory:', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS ways (oldway text, newway text, drive_mode text, dc int)''')
c.execute("INSERT INTO ways VALUES ('S','S','AUTO',0)")
conn.commit()

@app.route('/')
def index():
    return render_template('index.html', drive_mode='start')

@app.route('/start', methods=['POST'])
def man_auto():
    drive_mode=request.form.get('drive_mode')
    print(drive_mode)
    c.execute('SELECT drive_mode FROM ways')
    c.execute('''UPDATE ways SET drive_mode=?''',(drive_mode,))
    return render_template('index.html', drive_mode=drive_mode)

@app.route('/drive_manual', methods=['POST'])
def drive():
    c.execute('SELECT * FROM ways')
    (oldway, newway, drive_mode, dc) = c.fetchone()
    oldway=newway
    newway=request.form.get('newway')
    dist2obj = distance_detected(tdist=[])
    
    if newway=='brake':
        dc=dc-10
        if dc<0:
            dc=0
        newway = oldway
        
    if newway=='accel':
        dc=dc+10
        if dc>100:
            dc=100
        newway=oldway
    
    if newway=='S':
        dc=0

    if newway=='F' or newway=='B' or newway=='L' or newway=='R':
        pass

    if newway=='AUTO':
        newway='S'
        dc=0
        drive_mode="AUTO"

    c.execute('''UPDATE ways SET oldway=?, newway=?, drive_mode=?, dc=? ''', (oldway,newway,drive_mode,dc))
    conn.commit()
    c.execute('SELECT drive_mode FROM ways')
    all_one = c.fetchone()
    print('<-->', all_one)
    return render_template('index.html', speed=dc, drive_mode=drive_mode)


@app.route('/drive_auto', methods=['POST'])
def auto():
    stop_go=request.form.get('stop_go')
    print(stop_go)
    c.execute('SELECT * FROM ways')
    (oldway, newway, drive_mode, dc) = c.fetchone()
    print('>', oldway, newway, drive_mode, dc)
    if stop_go=='F':
        dc=30
        newway='F'
        oldway='F'
    if stop_go=='S':
        dc=0
        newway='S'
        oldway='S'   
    if stop_go=='MANUAL':
        dc=0
        drive_mode="MANUAL"
    print('->', oldway, newway, drive_mode, dc)
    c.execute('''UPDATE ways SET oldway=?, newway=?, drive_mode=?, dc=? ''', (oldway,newway,drive_mode,dc))
    conn.commit()
    c.execute('SELECT * FROM ways')
    all_one = c.fetchone()
    print('-->', all_one)
    return render_template('index.html', speed=dc, drive_mode=drive_mode)    

def loop_func():
    while True:
        c.execute('SELECT * FROM ways')
        (oldway, newway, drive_mode, dc) = c.fetchone()
        dist2obj = distance_detected(tdist=[])
        
        driveit(oldway, newway, drive_mode, dc, dist2obj)


#### START THREADS
try:
    t = threading.Thread(target=loop_func)
    t.daemon = True
    t.start()
except KeyboardInterrupt:
    GPIO.cleanup()
    
    

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)
  
#############################
# proccess auto drive response from html
# and convert to engine commands
    
def driveit(oldway, newway, drive_mode, dc, dist2obj):
    print('--->>>', newway, dc, dist2obj)
    
    if drive_mode=='MANUAL':
        if dist2obj < 25 and newway=='F':
            newway = 'S'
        if newway == 'F':
           motor.Motor_dc(dc,dc,0,0)    
        if newway ==  'B':
            motor.Motor_dc(0,0,dc,dc)
        if newway == 'S':
            dc=0
            motor.Motor_dc(0,0,0,0)
        if newway == 'L':
            motor.Motor_dc(0,dc,dc,0)
            sleep(3)
            if oldway=='F':
                motor.Motor_dc(dc,dc,0,0)
            if oldway=='B':
                motor.Motor_dc(0,0,dc,dc)
            oldway=newway          
        if newway == 'R':
            motor.Motor_dc(dc,0,0,dc)
            sleep(3)
            if oldway=='F':
                motor.Motor_dc(dc,dc,0,0)
            if oldway=='B':
                motor.Motor_dc(0,0,dc,dc)
            oldway=newway
        if dc==0:
            blink('off')
        else:
            blink('on')            
        sleep(0.1)

    if drive_mode=='AUTO':
        if dist2obj<25:
            print(dist2obj)
            motor.Motor_dc(0,0,dc,dc)
            print('going back')
            sleep(5)
            motor.Motor_dc(0,dc,dc,0)
            sleep(4)
            print('turning')
        if newway=='S':
            dc=0
        #if newway=='F':
            #dc=dc
        motor.Motor_dc(dc,dc,0,0)
        blink('on')            
