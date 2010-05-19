"""
TODO:

 * Be able to specify hosts on startup (command line or fall back to prompt before starting shell)
 * Special command to list/modify host list
 * cd support
  * Better relative directory support
  * tilde expansion
  * 'cd' for home dir shortcut support
 * Change prompt to show current directory
 * Handle errors
 * Have syntax for specifying a certain host by index or name
 * Document built-in commands
 * Allow for calling commands from the current fabfile
 * Better output readability
 
Wish list:
 * Completion in native shell (maybe use first host?)
"""
from __future__ import with_statement

import logging
log = logging.getLogger("fabsh")
import cmd
import sys
import os
from optparse import OptionParser

from fabric.api import *

class FabshInterpreter(cmd.Cmd):
    intro = "\nFabric Shell\n"
    prompt = "fabsh>: "
    
    def __init__(self, *args, **kwargs):
        self.cwd = ''
        cmd.Cmd.__init__(self, *args, **kwargs)
    
    def default(self, line):
        for host in env.hosts:
            env.host_string = host
            with cd(self.cwd):
                if line.startswith('cd '):
                    self.cwd = os.path.normpath(os.path.join(self.cwd, line[3:]))
                    log.debug("New cwd is %s" % self.cwd)
                    
                if line.startswith('sudo'):
                    sudo(line)
                else:
                    run(line)
        
    def do_set_hosts(self, line):
        print "set hosts: %s" % line
    
    def quit(self):
        sys.exit(0)
    
    def do_quit(self, line):
        quit()
    
    def do_exit(self, line):
        quit()

def main(args):
    parser = OptionParser()
    parser.add_option("-H", "--hosts", dest="host_list",
                      help="comma-separated list of hosts to operate on")

    (options, args) = parser.parse_args()
    if options.host_list:
        env.hosts = options.host_list.split(",")
    else:
        #TODO: Prompt the user for the host list here
        env.hosts = []
    
    
    interpreter = FabshInterpreter()
    interpreter.cmdloop()

if __name__=="__main__":
    sys.exit(main(sys.argv))