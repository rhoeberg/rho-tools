# content 0 = heading
# content 1 = scheduled etc..
# content 2 = scheduled etc..
#
# value = start datetime
# end = end datetime
#
# todo:
# - set alarms (probably using properties)

import sys
import icalendar
from PyOrgMode import PyOrgMode
from datetime import datetime, date, timedelta
from pytz import UTC # timezone
from os import path

# DEBUGGING
from pprint import pprint

uid_number = 0

def write_cal_file(cal, uid, dir):
    """
    """
    filename = "%s%s.ics" % (dir, uid)
    print("writting file: " + filename)
    f = open(filename, 'w+')
    f.write(cal.to_ical())
    f.close()
    
def get_cal_event_from_datetime(d):
    """
    """
    event = icalendar.Event()
    s= None
    e= None
    if d.format & d.TIMED:
        s= datetime(d.value.tm_year, d.value.tm_mon, d.value.tm_mday, d.value.tm_hour, d.value.tm_min)
        if d.end:
            e= datetime(d.end.tm_year, d.end.tm_mon, d.end.tm_mday, d.end.tm_hour, d.end.tm_min)
        else:
            e= datetime(d.value.tm_year, d.value.tm_mon, d.value.tm_mday, d.value.tm_hour, d.value.tm_min) + timedelta(hours=1)
    else:
        s= date(d.value.tm_year, d.value.tm_mon, d.value.tm_mday)
        if d.end:
            e= date(d.end.tm_year, d.end.tm_mon, d.end.tm_mday)
        else:
            e= date(d.value.tm_year, d.value.tm_mon, d.value.tm_mday) + timedelta(days=1)
    event.add('dtstart', s)
    event.add('dtend', e)
    event.add('dtstamp', datetime.now())
    return event

def create_ical_event(event, heading):
    event.add('summary', heading)
    global uid_number
    uid = "%i@%s" % (uid_number, path.basename(orgfile))
    event['uid'] =  uid
    uid_number+=1
    cal = icalendar.Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')
    cal.add_component(event)
    print('creating event: ' + heading)
    write_cal_file(cal, uid, caldir)


def scan_for_schedule(n):
    if is_schedule_element(n):
        summary = ""
        d = None
        if n.content[0].type & n.content[0].SCHEDULED:
            summary = "scheduled: " + n.heading
            d = n.content[0].scheduled
        elif n.content[0].type & n.content[0].DEADLINE:
            summary = "deadline: " + n.heading
            d = n.content[0].deadline
        # elif n.content[0].type & n.content[0].CLOSED:
            # summary = "closed: " + n.heading
            # d = n.content[0].closed
        if d != None:
            print('found event: ' + summary)
            event = get_cal_event_from_datetime(d)
            create_ical_event(event, summary)

    elif n.content and isinstance(n.content[0], str):
        d = PyOrgMode.OrgDate(n.content[0])
        if hasattr(d, 'value'):
            event = get_cal_event_from_datetime(d)
            summary = n.heading
            print('found event: ' + summary)
            create_ical_event(event, summary)
    else:
        for node in n.content:
            if hasattr(node, 'content'):
                scan_for_schedule(node)


def is_schedule_element(n):
    if not n.content:
        return False
    elif hasattr(n.content[0], 'TYPE') and n.content[0].TYPE == "SCHEDULE_ELEMENT":
        print("found schedule element")
        return True
    return False
        

if __name__ == '__main__':
    print("org file: " + sys.argv[1])
    orgfile = sys.argv[1]
    caldir = sys.argv[2]
    base = PyOrgMode.OrgDataStructure()
    base.load_from_file(orgfile)

    for n in base.root.content:
        if hasattr(n, 'content'):
            scan_for_schedule(n)
    print("---")
            
