import time
import curses
import subprocess
import sys
from datetime import datetime

# from curses.textpad import Textbox, rectangle
# from cursesmenu import *
# from cursesmenu.items import *

myscreen = curses.initscr()
curses.curs_set(0)
myscreen.nodelay(1)

# menu = CursesMenu("title", "subtitle")
# menu_item = MenuItem("Menu Item")
# menu.append_item(menu_item)# 
# # menu.show()



tseconds = 0
ttime = 0
timerOn = True
running = True
alarm_on = False

t1 = time.time()


# msg = ""

def my_raw_input(stdscr, r, c, prompt_string):
    curses.echo() 
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    input = stdscr.getstr(r + 1, c, 20)
    return input  #       ^^^^  reading input at next line  


def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

if __name__ == '__main__':
    from sys import argv
    myargs = getopts(argv)
    if '-t' in myargs:
        ttime = datetime.strptime(myargs['-t'], '%H:%M')
        timerOn = False
    if '-h' in myargs:
        tseconds += int(myargs['-h']) * 60 * 60
        print(tseconds)
    if '-m' in myargs:
        tseconds += int(myargs['-m']) * 60
        print(tseconds)
    if '-s' in myargs:
        tseconds += int(myargs['-s'])
        print(tseconds)
    if '-msg' in myargs:  # Example usage.
        # if myargs['-msg'] is not None:
        msg = myargs['-msg']
        # else:
            # msg = "alarm"
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

    # check if we should close

    c = myscreen.getch()
    if(c == 113):
        running = False;

    myscreen.erase()
    myscreen.border(0)

    # s = myscreen.getstr(0,0, 15)

    t2 = time.time()
    time_elapsed = t2 - t1

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
            # subprocess.call(['say', '-v', 'Samantha', msg])
            subprocess.call(['say', msg])
        else:
            m, s = divmod(tseconds - time_elapsed, 60)
            h, m = divmod(m, 60)
            myscreen.addstr(2, 1, "%d:%02d:%02d" % (h, m, s))
            myscreen.addstr(1, 1, msg)


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
            # with suspend_curses():
            # subprocess.call(['afplay', '/System/Library/Sounds/Purr.aiff'])
            # subprocess.call(['osascript', '-e', '\"set Volume 3\"'])
            subprocess.call(['say', '-v', 'Samantha', msg])
            # subprocess.call(['osascript', '-e', 'set Volume 10'])

    myscreen.refresh()

curses.endwin()


def poll_input():
    c = myscreen.getch()
    
