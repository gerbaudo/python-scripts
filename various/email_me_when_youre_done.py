#!/bin/env python

# email me when all my jobs on the queue are done
#
# davide.gerbaudo@gmail.com
# Oct 2013

import optparse
import os
from time import sleep
from utils import getCommandOutput

def main() :
    parser = optparse.OptionParser()
    parser.add_option('--from-address', default='dgerbaud@uci.edu')
    parser.add_option('--to-address',   default='davide.gerbaudo@gmail.com')
    parser.add_option('--message',      default='all jobs done, bam!')
    parser.add_option('--polleverysec', default=60*5, type='int')
    parser.add_option('--subject',      default='jobs done from `pwd`')
    parser.add_option('--user',         default=os.environ['USER'])
    parser.add_option('--exec-cmd', help='on completion, execute this command')
    (opts, args) = parser.parse_args() 
    receiver  = opts.to_address
    username  = opts.user
    message   = opts.message
    subject   = opts.subject
    everyNsec = opts.polleverysec
    nChecksDone = 0
    countJobsCmd="qstat -u %(user)s | grep %(user)s | egrep '(Q|R)' | wc -l"% {'user':username}
    nJobsRunning = int(getCommandOutput(countJobsCmd)['stdout'])    
    while nJobsRunning > 0 :
        sleep(everyNsec)
        nJobsRunning = int(getCommandOutput(countJobsCmd)['stdout'])
        nChecksDone += 1
    preamble = "From: %s \n"%opts.from_address
    
    message = preamble+message
    message += ("\n(after %(nchk)d checks every %(nsec)d sec)"
                %{'nchk' : nChecksDone, 'nsec' : everyNsec})
    subject = opts.subject
    mailCmd = ("echo -e \"%(msg)s\" | mail -s \"%(sbj)s\" %(dest)s"
               % {'dest' : receiver, 'msg' : message, 'sbj':subject})
    print mailCmd
    getCommandOutput(mailCmd)
    if opts.exec_cmd:
        print "now executing {}".format(opts.exec_cmd)
        out = getCommandOutput(opts.exec_cmd)
        print out['stdout']
        print out['stderr']

if __name__=='__main__' :
    main()
