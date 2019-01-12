import sys
from PyOrgMode import PyOrgMode
import subprocess

# def getopts(argv):
#     opts = {}
#     while argv:
#         if argv[0][0] == '-':
#             opts[argv[0]] = argv[1]
#         argv = argv[1:]
#     return opts
def add_todo(base, heading):
    new_todo = PyOrgMode.OrgNode.Element()
    new_todo.heading = todo_heading
    new_todo.level = 1
    new_todo.todo = "TODO"
    base.root.append_clean(new_todo)
    base.save_to_file(orgfile)

if __name__ == '__main__':
    from sys import argv
    # myargs = getopts(argv)
    orgfile = sys.argv[1]
    todo_heading = sys.argv[2]
    base = PyOrgMode.OrgDataStructure()
    base.load_from_file(orgfile)
    add_todo(base, todo_heading)
    for n in base.root.content:
        print(n)
    


