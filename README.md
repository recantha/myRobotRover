# myRobotRover
This is a project to create a robot car to move either autonomously or driven through a web interface.
It utilises Flask for the web interface and the motion lib (https://motion-project.github.io/index.html)  for streaming a video image to the same web interface as the movement control commands.

As Flask does not allow for public variables (tried many different approaches) I had to resort to using a single sqlite3 table ('ways') held in memory (no read/write to physical diskfile).

Istalling sqlite3 is easy:

    $ sudo apt-get install sqlite3

And it is initialised by:

    conn = sqlite3.connect(':memory:', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ways (oldway text, newway text, drive_mode text, dc int)''')
    c.execute("INSERT INTO ways VALUES ('S','S','AUTO',0)")
    conn.commit()


I then either READ:

    c.execute('SELECT * FROM ways')
    (oldway, newway, drive_mode, dc) = c.fetchone()
    
or read and then UPDATE the table:

    c.execute('''UPDATE ways SET oldway=?, newway=?, drive_mode=?, dc=? ''', (oldway,newway,drive_mode,dc))
    conn.commit()
    
depending on whether I need to retrieve the motor movement commands or store the new values.

Finally I use threading so that I can continuously read  the distance from an obstructing object.
The code seems to work but there is appreciable lag from the command given by the web interface to execution. The main problem however is the erratic behaviour of the engines which once started they run / stop /run again with different speed to the one expected

If cloning change to whatever dir you clone to and use the commands for motion and the pi camera included in  my.sh file
