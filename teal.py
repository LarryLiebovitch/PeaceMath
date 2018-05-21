"""
HELLO, I am teal.py

-------------------------------------------------------------------------------
MIT License Copyright (c) 2017 Larry S. Liebovitch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-------------------------------------------------------------------------------

GUI to integrate ordinary differential equations (ODEs)
Display the results
Change the initial conditions or interactions between variables

ODEs: dx(i)/dt = m(i)x(i) + b(i) + SUM(j)[c(i,j)tanh(x(j)]
    x(i) = system variables
    m(i) = decay time scale
    b(i) = self or external influence
    c(i,j) = adjacency matrix, the effect of j on i
    ic(i) = initial conditions
    numerically integrated by Euler integration step size dt
    
SCRIPTS: PYTHON 3.4.1 (later 3.6.1) with Tkinter
data.py
teal.py
tealclass.py

DATAFILES (# = 8, 105, 111, 202)
m#.txt = m(i)
b#.txt = b(i)
ic#.txt = ic(i)
c#.txt = c(i,j)
btextbxy#.txt =
    variable name, color, (x,y) from upper left corner, height, width
    
-----------------------------------------------------------------------------   

FIRST RUN THE SCRIPTS:
    data.py
    tealclass.py
    
THEN RUN THE SCRIPT:
    teal.py
        When asked for "ONLY NUMBER n and I will find cn.txt, etc. (#/a, Def=a)"
            type either:
            8 <RETURN>
            105 <RETURN>
            111 <RETURN>
            202 <RETURN>
        When asked for "Want to CHANGE parameters (y/n), def=n"
            type: <RETURN>

TO CHANGE INITIAL CONDITIONS:
use the left hand entry widgets and click on ENTER

TO CHANGE THE CONNECTION MATRIX:
click on a textbox, use the left hand entry widget, and click ENTER
(this will also show only the links into and out of that textbox,
click on  ALL Cij to show all the links)

TO RUN THE CALCULATION:
click CALCULATE

TO SWITCH FROM THE LINKS TO THE INITIAL CONDITIONS:
click on IC on the links input

TO RESTORE THE ORIGINAL INITIAL CONDITIONS:
click on ORIGINAL on the initial conditions input

-----------------------------------------------------------------------------   
"""

import math
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import random
import time
import data as pass_data
from tealclass import * #import the METHODS from tealclass.py


#START OF DEFINED FUNCTIONS----------------------------------------------------
#read text string in a file
def filein (fname):
    numlines=0
    xin=[]
    f=open(fname,'r')
    for line in f:
        #print (line, end='')
        xin.append(line)
        numlines=numlines+1
    f.close()
    return xin,numlines

#not used
#writes text string to file
def fileout (filename,filedata):
    f2=open(filename,'w')
    f2.write(filedata)
    f2.close()

#not used
#parses text tables with 2 columns
#x,y separated by a TAB
#rows separated by a RETURN
def getxy (fname):
    data,numlines=filein(fname)
    x=['0' for i in range(numlines)]
    y=['0' for i in range(numlines)]
    for i in range(numlines):
        xline=data[i]
        xline2=xline.split('\t')
        xline2[-1]=xline2[-1].replace('\n','')
        #print ('\nxline2',xline2)
        x[i]=eval(xline2[0])
        y[i]=eval(xline2[1])
    return x,y,numlines

#parse files m#.txt, b#.txt, c#.txt
def getx (fname):
    data,numlines=filein(fname)
    #print ('\ndata\n',data,'\nlines',numlines)
    x=['0' for i in range(numlines)]
    for i in range(numlines):
        x[i]=data[i].replace('\n','')
        x[i]=eval(x[i])
    return x,numlines

#parse file c#.txt
#reads any text table with n columns
#elements in a row separated by a TAB
#rows separated by a RETURN
def getxn(fname):
    data,numlines=filein(fname)
    dataline=['0' for i in range(numlines)]
    for i in range(numlines):
        x=data[i]
        y=x.split('\t')
        y[-1]=y[-1].replace('\n','')
        dataline[i]=y
    #print ('\n\nascii-input',dataline)
    xdata=dataline[:]
    for i in range (numlines):
        inline=len(dataline[i])
        for j in range (inline):
            if xdata[i][j] != '':
                xdata[i][j]=eval(xdata[i][j])
            else:
                xdata[i][j]=None
    #print ('dataline',dataline)
    #print ('xdata',xdata)
    return xdata, numlines
    
#parse file btextbxy#.txt
def getxnsecondstring(fname):   #get n inputs from each line
#variable name, color, (x,y) from upper left corner, height, width
    data,numlines=filein(fname)
    dataline=['0' for i in range(numlines)]
    for i in range(numlines):
        x=data[i]
        y=x.split('\t')
        y[-1]=y[-1].replace('\n','')
        dataline[i]=y
    #print ('\n\nascii-input',dataline)
    xdata=dataline[:]
    for i in range (numlines):
        inline=len(dataline[i])
        for j in range (2,inline):
            if xdata[i][j] != '':
                xdata[i][j]=eval(xdata[i][j])
            else:
                xdata[i][j]=None8                
    #print ('dataline',dataline)
    #print ('xdata',xdata)
    return xdata, numlines

#fancy way to easily change input values
def lslin(invars,invar):
    print('\ncurrent value of ',invars,' is= ',invar)
    outvars=input('\nchange to (def=no change)')
    if (outvars==''):
        return invar
    else:
        outvar=eval(outvars)
    return outvar
#END OF DEFINED FUNCTIONS------------------------------------------------------


#START DATA INPUT
fast=input('\n ONLY NUMBER n and I will find cn.txt, etc. (#/a, Def=a)')
#give it just a number # and RETURN and it will read files:
# m#.txt, b#.txt, ic#.txt, c#.txt, and btextbxy#.txt
if fast.isdigit():
    fnamec='c'+fast+'.txt'
    fnameb='b'+fast+'.txt'
    fnamem='m'+fast+'.txt'
    fnameic='ic'+fast+'.txt'
    fnamebtextbxy='btextbxy'+fast+'.txt'
else:
    fname=input('\nfilename for array c [I will add .txt]=  ')
    fnamec=fname+'.txt'
    
    fname=input('\nfilename for array b [I will add .txt]=  ')
    fnameb=fname+'.txt'
    
    fname=input('\nfilename for array m [I will add .txt]=  ')
    fnamem=fname+'.txt'
    
    fname=input('\nfilename for array IC [I will add .txt]=  ')
    fnameic=fname+'.txt'
    
    fname=input('\nfilename for bxy, btext [I will add .txt]=  ')
    fnamebtextbxy=fname+'.txt'

#get the input from the files
c,numc=getxn(fnamec)
b,numb=getx(fnameb)
m,numm=getx(fnamem)
ic,numic=getx(fnameic)
btextbxydata,numvar=getxnsecondstring(fnamebtextbxy)

#check for consistentcy
if (numc**4!=numb*numm*numic*numvar):
    print ("\nFATAL WARNING - input issue - numbers c,b,m,ic,bxy,btext don't match")
    quit()

#PART ONE make original m, b, c, ic arrays (NOT matrices) and print
ma=np.array(m)
ba=np.array(b)
ca=np.array(c)
ica=np.array(ic)
print ('\nca= ',ca)
print ('\nba= ',ba)
print ('\nma= ',ma)
print ('\nica= ',ica)

change=input('\nWant to CHANGE parameters (y/n), def=n')
if (change=='y' or change=='Y'):
    c=lslin('c',c)
    b=lslin('b',b)
    m=lslin('m',m)
    ic=lslin('ic',ic)
    
    ma=np.array(m)
    ba=np.array(b)
    ca=np.array(c)
    ica=np.array(ic)
    print ('\n\nNEW PARAMTER VALUES ARE:')
    print ('\nca= ',ca)
    print ('\nba= ',ba)
    print ('\nma= ',ma)
    print ('\nic= ',ica)
else:
    pass

#PART TWO read in the variable names and box size and locations in the plot
print('\n numvar(from btextbxy)= ',numvar)
print('\n btextbxydata= ',btextbxydata)

#COMPUTE (x,y)=[0,1] needed from PPTX
bx=[btextbxydata[i][2] for i in range (numvar)]
by=[btextbxydata[i][3] for i in range (numvar)]
wx=[btextbxydata[i][5] for i in range (numvar)]
hy=[btextbxydata[i][4] for i in range (numvar)]

#note this scaling has changed 2017-07-06
#SCALE as needed for the plot
xp=[0. for i in range(numvar)]
yp=[0. for i in range(numvar)]
xp2=[0. for i in range(numvar)]
yp2=[0. for i in range(numvar)]
for i in range(numvar):
    xp[i]=(bx[i] + 0.5*wx[i])
    yp[i]=(by[i] + 0.5*hy[i])
maxx,minx=max(xp),min(xp)
maxy,miny=max(yp),min(yp)
for i in range(numvar):
    xp2[i]=0.9*(xp[i]-minx)/(maxx-minx)+0.05
    yp2[i]=1-(0.9*(yp[i]-miny)/(maxy-miny)+0.05)
    
bxy=[[xp2[i],yp2[i]] for i in range(numvar)]
print ('\nbxy=  ',bxy)

#PARAEMTERS NEEDED FOR THE NUMERICAL INTEGRATION
dt=.001 #step size
numdata=30000 #number of integration steps
t=[0. for i in range(numdata)] #time
z=np.array([ica for i in range (numdata)]) #row=variables at each time

#READY TO PASS ON DATA----------------------------------------------------------
#wrap parameters to pass into function 
pass_data.numdata=numdata
pass_data.ca=ca
pass_data.dt=dt
pass_data.ma=ma
pass_data.ba=ba
pass_data.numc=numc
pass_data.z=z
pass_data.t=t
pass_data.ica=ica
#NEW DATA's ADDED BELOW
pass_data.fnamec=fnamec
pass_data.fnamem=fnamem
pass_data.fnameb=fnameb
pass_data.fnamebtextbxy=fnamebtextbxy
pass_data.dt=dt
#EVEN MORE DATA'S ADDED BELOW
pass_data.a=ca
pass_data.bxy=bxy
pass_data.btext=str([btextbxydata[i][0] for i in range(numvar)])
pass_data.b=ica
pass_data.labels=[btextbxydata[i][0] for i in range(numvar)]
#ADDING BOX COLORS
pass_data.boxcolor=[btextbxydata[i][1] for i in range(numvar)]


#call the classes----------------------------------------------
zzz=App()
#call the classes----------------------------------------------
