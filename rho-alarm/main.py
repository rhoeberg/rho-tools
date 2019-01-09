import time
import curses
import subprocess
import sys
from datetime import datetime

myscreen = curses.initscr()
curses.curs_set(0)
myscreen.nodelay(1)

tseconds = 0
ttime = 0
running = True
alarm_on = False
t1 = time.time()

def my_raw_input(stdscr, r, c, prompt_string):
    curses.echo() 
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    input = stdscr.getstr(r + 1, c, 20)
    return input

def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
        argv = argv[1:]
    return opts

if __name__ == '__main__':
    from sys import argv
    myargs = getopts(argv)
    if '-t' in myargs:
        ttime = datetime.strptime(myargs['-t'], '%H:%M')
        ttime = ttime.replace(year = datetime.today().year)
        ttime = ttime.replace(month = datetime.today().month)
        ttime = ttime.replace(day = datetime.today().day)
        tseconds = time.mktime(ttime.timetuple()) - time.mktime(datetime.today().timetuple())
        if (tseconds < 0):
            tseconds += 24*60*60
    if '-h' in myargs:
        tseconds += int(myargs['-h']) * 60 * 60
    if '-m' in myargs:
        tseconds += int(myargs['-m']) * 60
    if '-s' in myargs:
        tseconds += int(myargs['-s'])
    if '-msg' in myargs:
        msg = myargs['-msg']
    else:
        msg = "alarm"
        
    print(myargs)

class suspend_curses():
    """Context Manager to temporarily leave curses mode"""

    def __enter__(self):
        curses.endwin()

    def __exit__(self, exc_type, exc_val, tb):
        newscr = curses.initscr()
        newscr.addstr('Newscreen is %s\n' % newscr)
        newscr.refresh()
        curses.doupdate()

while running:
    # poll input
    c = myscreen.getch()

    # check if we should close
    if(c == 113):
        running = False;

    myscreen.erase()
    myscreen.border(0)
    
    t2 = time.time()
    time_elapsed = t2 - t1

    if (alarm_on == True):
        myscreen.addstr(1, 1, msg, curses.A_BLINK)
        myscreen.addstr(2, 1, "q = quit")
        myscreen.addstr(3, 1, "1 = snooze 10")
        myscreen.addstr(4, 1, "2 = snooze custom")
        if(c == 49):
            alarm_on = False
            tseconds = 10 * 60
            t1 = time.time()
        elif(c == 50):
            myscreen.nodelay(0)
            s = myscreen.getstr(0,0, 15)
            myscreen.nodelay(1)
            alarm_on = False
            tseconds = int(s) * 60
            t1 = time.time()
        if((round(time_elapsed,1) % 60) == 0.0):
            subprocess.call(['say', '-v', 'Samantha', msg])

    if(alarm_on == False):
        myscreen.addstr(3, 1, "q = quit")
        if (time_elapsed > tseconds):
            h = 0 
            m = 0 
            s = 0
            myscreen.addstr(2, 1, "%d:%02d:%02d" % (h, m, s))
            alarm_on = True;
            t1 = time.time()
            subprocess.call(['terminal-notifier', '-message', msg])
            subprocess.call(['say', '-v', 'Samantha', msg])
        else:
            m, s = divmod(tseconds - time_elapsed, 60)
            h, m = divmod(m, 60)
            myscreen.addstr(2, 1, "%d:%02d:%02d" % (h, m, s))
            myscreen.addstr(1, 1, msg)

    myscreen.refresh()
curses.endwin()
