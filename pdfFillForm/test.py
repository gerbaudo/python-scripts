#!/bin/env python

# export PYTHONPATH=$PYTHONPATH:`pwd` 

from fdfgen import forge_fdf

fields = [
    ('Date','my date'),
    ('Print name','a print name'),
    ('Print address','an address'),
    ('undefined','something'),
    ('Editor','my editor'),
    ('ESSAY OR CHAPTER TITLE','AA chapeter title'),
    ('BOOK TITLE','AA book title')
    ]

#fields = [('name','John Smith'),('telephone','555-1234')]
fdf = forge_fdf("",fields,[],[],[])
fdf_file = open("data.fdf","w")
fdf_file.write(fdf)
fdf_file.close()
