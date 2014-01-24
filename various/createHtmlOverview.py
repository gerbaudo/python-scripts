#!/bin/env python
#
# A simple script to create an html page with an overview of the directory tree.
# This script walks recursively the directory tree and for each sub-directory
# it creates an 'index.html' page which will contain:
# - an overview of the subdirectories
# - a dump of the text files
# - a table (currently with two items per row) with all the images scaled to
#   some predefined size (currently 400px X 300px)
#
# davide.gerbaudo@gmail.com, Jan2011
#
# -----------
# | License |    GPLv3 (http://www.gnu.org/licenses/gpl.html)
# -----------
#
# Todo:
# - add an option not to overwrite the current index.html, or to skip
#   the directories that already have an index.html file.
# - pass the hardcoded parameters on the command line.
# - add link to "one level up"
# - indent the html based on the directory depth

import os,sys,commands
from optparse import OptionParser

class Directory:
    """A directory object which knows its name, parent, and has a list of daughters.
    The directory might also have a short description associated with it,
    saying shortly what its contets are."""
    def __init__(self,name,parent='',shortDescriptionFile="shortdescription.txt",verbose=False, overwrite=True):
        "Constructor"
        self.name_  = name
        self.overwrite = overwrite
        self.parent_ = parent
        self.verbose_ = verbose
        self.shortDescFile_ = shortDescriptionFile
        self.shortdescription_ = ""
        self.readDescFile(self.getBasePath()+"/"+self.shortDescFile_)
        self.populateDaughterList()
    def depth(self):
        "depth in the directory tree"
        if not self.parent_ : return 0
        else: return self.parent_.depth()+1
    def readDescFile(self, filename):
        "Read the file containing the one-line description of the directory's contents"
        if os.path.isfile(filename):
            self.description_ = open(filename).read()
            if self.verbose_ : print self.description_
        elif self.verbose_ : print "'%s' without description file '%s'" % (self.name_, self.shortDescFile_)
    def populateDaughterList(self):
        "Populate the list of daughters directories"
        self.daughters_ = []
        basepath = self.getBasePath()
        names = os.listdir(basepath)
        for name in names:
            if os.path.isdir(basepath+'/'+name):
                self.daughters_.append(Directory(name,self,self.shortDescFile_,self.verbose_))
        if self.verbose_ : print "%s contains %d directories" % (self.name_,len(self.daughters_))
    def getBasePath(self):
        "Return a basepath by asking the parents where we are"
        if not self.parent_ : return "./"
        else: return self.parent_.getBasePath()+"/"+self.name_
    def htmlSubDirectoryTree(self,relativeTo=None):
        """Print an html unnumbered list showing the subdirectories of this directory.
        If relativeTo=="", the links will be relative to this directory.
        Otherwise they will be relative to the provided basepath."""
        if self.verbose_ : print "->%s.htmlSubDirectoryTree(%s)" % (self.name_, relativeTo)
        text = ""
        # if this dir does not have a parent, then it needs to open an 'ul' on its own
        if not self.parent_ : text +=  "<ul>\n"
        if len(self.daughters_) : text += "<ul>\n"
        for daughter in self.daughters_:
            text += "<li>\n"
            target=""
            label=""
            if not relativeTo:
                target="%s/index.html"%daughter.name_
                label=daughter.name_
            else:
                target="%s/%s/index.html"%(relativeTo,daughter.name_)
                label=daughter.name_
            if self.verbose_:print "adding '%s' --> '%s'" % (label,target)
            text += "<a href=\"%s\">%s</a>\n" % (target,label)
            if hasattr(daughter,"description_") and len(daughter.description_):
                text += daughter.description_
            text += "</li>\n"
            # when we are done with the 1st gen daughters, do the same recursively
            relPath=""
            if not self.parent_ : relPath="%s/%s"%(self.name_,daughter.name_)
            elif not relativeTo : relPath="%s/%s"%(self.name_,daughter.name_)
            else : relPath="%s/%s"%(relativeTo,daughter.name_)
            if self.verbose_:
                print "calling htmlSubDirectoryTree for daughter '%s' with relativeTo='%s'"\
                    %\
                    (daughter.name_, relPath)
            text += daughter.htmlSubDirectoryTree(relPath)
        if len(self.daughters_) : text += "</ul>\n"
        # if this dir does not have a parent, then it needs to close an 'ul' on its own
        if not self.parent_ : text +=  "</ul>\n"
        return text

    def htmlHeader(self):
        "Print the html header"
        return '\n'.join(['<html>',
                          '<head>',
                          '   <title>Directory tree</title>',
                          '<!-- Generated with createHtmlOverview.py -->',
                          '</head>',
                          '<body>'])
    def htmlFooter(self):
        "Print the html footer"
        return '\n'.join(['</body>',
                          '</html>'])
    def findImages(self):
        "Find the images in this directory"
        imgExtensions = ["png", "jpg", "gif"]
        imgFiles = []
        for ext in imgExtensions:
            files = os.listdir(self.getBasePath())
            for file in files:
                if file.count(ext) and not file.count("No such file"):
                    imgFiles.append(file)
        return imgFiles
    def findExtFiles(self, extensions=[]):
        "find the txt files in this directory"
        def isFileWithExt(f, extensions=extensions, ignore=[self.shortDescFile_,]) :
            return any(f.endswith(e) for e in extensions) and not any(f==n for n in ignore)
        return sorted(filter(isFileWithExt, os.listdir(self.getBasePath())))
    def findTxtFiles(self):
        return self.findExtFiles(extensions=['txt'])
    def getImgTable(self):
        "Provide an html table showing the images of this directory"
        nColumns = 2
        thumbWidth=400
        thumbHeight=300
        #thumbHeight=400
        imgFiles = self.findImages()
        if self.verbose_: print "%s %d images" % (self.name_,len(imgFiles))
        if not len(imgFiles): return ""
        htmlBody = ""    
        htmlBody += "<table cellspacing=\"10\">\n"
        htmlBody += "<tr>\n"
        for imgFile in imgFiles:
            htmlBody += "<td>\n"
            htmlBody += "<a href=\"%s\">" % imgFile
            htmlBody += "<img src=\"%s\" width=\"%d\" height=\"%d\">" % (imgFile, thumbWidth, thumbHeight)
            htmlBody += "</img>"
            htmlBody += "<br>\n"
            htmlBody += "<h4>%s</h4>" % imgFile[:imgFile.rfind(".")]
            htmlBody += "</a>\n"
            htmlBody += "</td>\n"
            if (imgFiles.index(imgFile)+1) % nColumns == 0:
                htmlBody += "</tr>\n<tr>\n"
        htmlBody += "</tr>\n"
        htmlBody += "</table>\n"
        return htmlBody
    def getTxtFilesDump(self):
        "Get a preformatted dump of the txt files in this directory"
        txtFiles = self.findTxtFiles()
        text = ""
        basepath = self.getBasePath()
        if len(txtFiles)>0:
            for txtFile in txtFiles:
                text += "<pre>"
                text += commands.getoutput("cat %s/%s" % (basepath, txtFile))
                text += "</pre>"
        return text
    def ulistPdf(self) :
        pdfFiles = self.findExtFiles(extensions=['pdf'])
        return '<ul>\n'+'\n'.join(['<li><a href="%s">%s</a></li>'%(f,f) for f in pdfFiles])+'\n</ul>\n'

    def createHtmlIndex(self, outfile="index.html"):
        """This function creates an index.html page with (in this order):
        - a list of the subdirectories
        - a dump of the txt files in this directory
        - a table with all the images
        This function is also called recursively for all subdirectories"""
        filename = self.getBasePath()+"/"+outfile
        if not self.overwrite and os.path.exists(filename) : return
        file = open(filename, 'w')
        file.write(self.htmlHeader()+"\n")
        file.write(self.htmlSubDirectoryTree()+"\n")
        file.write(self.ulistPdf()+"\n")
        file.write(self.getTxtFilesDump()+"\n")
        file.write(self.getImgTable()+"\n")
        file.write(self.htmlFooter()+"\n")
        file.close()
        if hasattr(self,"daughters_"):
            for daughter in self.daughters_:
                daughter.createHtmlIndex()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      default="./",
                      help="top level input directory")
    parser.add_option("--do-not-overwrite", dest="overwrite",
                      default=True, action="store_false",
                      help="do not overwrite existing index.html files")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print status messages to stdout")

    (options, args) = parser.parse_args()

    verbose = options.verbose
    inputDir = options.input
    overwrite = options.overwrite
    topDir = Directory(inputDir,verbose=verbose,overwrite=overwrite)
    topDir.createHtmlIndex()
