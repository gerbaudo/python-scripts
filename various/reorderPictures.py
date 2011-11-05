#!/bin/env python
#
# August 2011
# davide.gerbaudo@gmail.com
#
# Simple script to re-order pictures in monthly subfolders
# Usage:
# $ reorderPictures.py inputDir outputDir
#


import os, sys
import commands
import time

def collectFileNames(inputDir):
    "get a list of filenames from a directory"
    cmd = "find %s -type f" % inputDir
    interestingText = commands.getoutput(cmd)
    filenames =  interestingText.split("\n")
    return filenames

if __name__=="__main__":

    verbose = False
    dryRun = True
    # parse cmd-line
    if len(sys.argv) < 3:
        print "Usage: %s inputDir outputDir" % sys.argv[0]
        sys.exit(0)
    if "--move" in sys.argv:
        dryRun = False
    inputDir = sys.argv[1]
    outputDir = sys.argv[2]
    # check directories
    if not os.path.isdir(inputDir) or not os.path.isdir(outputDir):
        print "One of the specified paths is not a directory."
        sys.exit(0)

    # collect filenames and do the job
    fileNames = collectFileNames(inputDir)
    for fileName in fileNames:
        ctime = os.path.getmtime(fileName)
        year = time.strftime("%Y",time.gmtime(ctime))
        month = time.strftime("%b",time.gmtime(ctime))
        destDir = "%s/%s/%s" % (outputDir, year, month)
        if not os.path.isdir(destDir):
            if verbose:
                print "# creating dir %s" % destDir
            cmd = "mkdir -p %s" % destDir
            print cmd
            if not dryRun:
                commands.getoutput(cmd)
        cmd = "mv %s %s" % (fileName, destDir)
        print cmd
        if not dryRun:
            commands.getoutput(cmd)

    if dryRun:
        print "This was a dry run."
        print "Please run with '--move' to actually move the files."

