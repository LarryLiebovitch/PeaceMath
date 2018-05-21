"""
HELLO, I am tealclass.py

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

import tkinter as tk
import data
import numpy as np
from decimal import *
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg


#Defines the textboxes that will scale to the size of the variables x(i)
class TextBox:
    list_box=[]  
    selected_box_id=-1
    colors = ['#FFFFFF','#E0F3FC','#CFECF9','#BCE5F7','#ABDAF4','#9FD0F0', '#9AC7E7','#96C3E2','#92BEDC','#8FB9D7','#8BB4D1','#87B0CC','#84ABC6','#80A6C1','#7CA1BB','#789CB5','#7497AF','#7092AA','#6C8DA4','#698AA0','#65859B','#5C798E','#587488','#557185','#506B7D','#4C6678','#486172','#445C6D','#405767','#3B5161']

    def __init__(self,ax13,x,y,s,id,t,boxcolor):
        self.x = x
        self.y = y
        self.size = s
        self.id = id
        self.boxcolor=boxcolor #adding color
        self.text=ax13.text(x, y, t, style='italic',horizontalalignment='center',verticalalignment='center',size=s, color='k',transform=ax13.transAxes,bbox={'facecolor':self.colors[0], 'pad':10})
        self.text.set_bbox(dict(facecolor=boxcolor,alpha=0.2,edgecolor='black'))
        self.list_box.append(self)

    def setXY(self, x,y):
        self.x=x
        self.y=y

    def setSize(self, s):
        self.size=s
        self.text.set_fontsize(s)


#Defines the arrows used to connect the textboxes
#note some of the fancy arrow paramters changed from their default values
class ArrowObject:
    ''' @f from which box
        @t to which box
    '''
    visible_arrow=[]
    def __init__(self,ax13,f,t,id):
        self.from_box = f
        self.to_box = t
        self.id = id
        end=(data.bxy[f][0],data.bxy[f][1])
        start=(data.bxy[t][0],data.bxy[t][1])
        amin, amax=np.amin(abs(data.a)), np.amax(abs(data.a))
        opacity=(abs(data.a[f][t])-amin)/(amax-amin)*.8 +.2
        # width=opacity*24/data.numc #scale ARROW WIDTH inverse #VARIABLES
        width=opacity*(24.+(2./3.)*(data.numc-6.))/data.numc # a BETTER scale?
        if data.a[f][t]<0:
            arrow_color='r'
        else:
            arrow_color='#00ccff'
        self.arrow=patches.FancyArrowPatch(
            start,
            end,
            connectionstyle='arc3, rad=0.1',
            color = arrow_color,
            shrinkB=10,
            shrinkA=10,
            alpha=opacity,
            linewidth=width)
        self.arrow.set_arrowstyle('fancy',head_length=6*width, head_width=6*width)
        if data.a[f][t]!=0:
            self.visible_arrow.append(self)
        ax13.add_patch(self.arrow)
        

#MAIN CLASS THAT DOES MOST OF THE WORK
class App:
    #constructor
    def __init__(self):
        self.data=data
        self.fewarrows=0
        self.MakeWindow()
        self.refreshDataFrame()
        self.refreshPicFrame()
        self.fixent=1 #UGLY FIX FOR ENTRIES/ENTRIESIJ
        # self.root.mainloop() -maybe needed for Windows OS


    #makes frames and frames within frames needed for correct display
    def MakeWindow (self):
        self.root=tk.Tk()
        self.root.wm_title("Data Input and Graphical Output")
        self.outsideframed1=tk.Frame(self.root,width=300, height=800)
        self.outsideframepic=tk.Frame(self.root,width=675, height=800)
        self.outsideframed1.pack(side=tk.LEFT,fill=None,expand=False)
        self.outsideframepic.pack(side=tk.LEFT,fill=None,expand=False)                                 
        self.outsideframed1.pack_propagate(False) 
        self.outsideframepic.pack_propagate(False)      
        self.framed1=tk.Frame(self.outsideframed1,width=200, height=100)
        self.framed1.pack(side=tk.LEFT,fill=None,expand=False)
        self.framepic=tk.Frame(self.outsideframepic,borderwidth=5,relief=tk.RIDGE)
        self.framepic.pack(side=tk.TOP,fill=tk.BOTH,expand=1) #BIG-BAD
        self.refreshDataFrame()
        self.refreshPicFrame()

    
    #makes the plot: boxes and the (fancy) arrows connecting them
    def createBoxGraph(self):
        TextBox.list_box=[]  #CLEAR ALL PREVIOUS!!!
        f = plt.figure(facecolor = 'white')
        f.set_size_inches(8,10)
        a = f.add_subplot(111)
        a.axis('off')
        for index in range(len(data.b)):
            xy=data.bxy[index]
            TextBox(a,xy[0],xy[1],data.b[index],index,data.labels[index],data.boxcolor[index])
        id=0
        if (self.fewarrows==0):
            for i in range(len(data.b)):
                for j in range(len(data.b)):
                    if i!=j and data.a[i][j]!=0:
                        arrow=ArrowObject(a,i,j,id)
                        id=id+1
        else:
            i=self.box_id
            for j in range(len(data.b)):
                if i!=j and data.a[i][j]!=0:
                    arrow=ArrowObject(a,i,j,id)
                    id=id+1
            j=self.box_id
            for i in range(len(data.b)):
                if i!=j and data.a[i][j]!=0:
                    arrow=ArrowObject(a,i,j,id)
                    id=id+1
        plt.show(block=False)
        #coding trick to close extra figures accidentally created in canvas----
        openfigs=plt.get_fignums()
        last=openfigs[-1]
        plt.close(last)
        #coding trick to close extra figures accidentally created in canvas----
        return f

    
    #used to scale the sizes of the textboxes
    def scalebox(vector):
        data2=[0 for i in range(len(vector))]
        minbox,maxbox=2,30
        minb,maxb=min(vector),max(vector)
        if minb!=maxb:
            data2=[(vector[i]-minb)/(maxb-minb) for i in range(len(vector))]
            vectornew=[(maxbox-minbox)*data2[i]+minbox for i in range(len(vector))]
        else:
            vectornew=[(minbox+maxbox)/2. for i in range(len(vector))]
        return vectornew


    #Euler numerical integration of the ordinary differential equations
    def recalculate(self,pass_data):
        #UGLY FIX FOR ENTRIES/ENTRIESIJ----------------------------------------
        if self.fixent==1:
            self.data.z[0]=[eval((self.entries[i][1].get())) for i in range(len(self.entries))]
        if self.fixent==2:
            column=[eval((self.entriesIJ[i][1].get())) for i in range(len(self.entriesIJ))]
            self.data.ca[:,self.box_id]=column
        #UGLY FIX FOR ENTRIES/ENTRIESIJ----------------------------------------
        self.fewarrows=0
        pass_data.tt=0
        for i in range (1,pass_data.numdata):
            mtanh=np.tanh(pass_data.z[i-1])
            cterm=np.dot(pass_data.ca,mtanh)
            pass_data.dx=pass_data.dt*(pass_data.ma*pass_data.z[i-1] + pass_data.ba + cterm)
            pass_data.tt=pass_data.tt+pass_data.dt
            pass_data.t[i]=pass_data.tt
            pass_data.z[i]=pass_data.z[i-1]+pass_data.dx
            for j in range(pass_data.numc):
                pass_data.z[i][j]=max(pass_data.z[i][j],0.) 
        #make new plot
        App.MakePlot(data)
        #scale b's from z[-1]
        vector=data.z[-1]
        data.b=App.scalebox(vector)
        #set z[0]=z[-1] for the NEXT iteration
        pass_data.z[0]=pass_data.z[-1]
        #CLEAR and REFRESH DATA and PIC frames
        App.ClearFrame(self.framed1)
        App.ClearFrame(self.framepic)
        self.refreshDataFrame()
        self.refreshPicFrame()        
     
        
    #makes plot of x(i) vs. time
    def MakePlot(pass_data):
        print('\nYour plot is ready')
        localtime = time.asctime( time.localtime(time.time()) )
        x_start=pass_data.z[0]
        x_final=pass_data.z[-1]
        plt.figure()
        plt.axes([0.1,.075,.8,.7])
        plt.plot(pass_data.t,pass_data.z[:,0:pass_data.numc])
        #print labels on lines
        xtext=25
        for i in range (pass_data.numc):
            ytext=pass_data.z[-1,i]
            varis=str(i) #first variable is 0
            plt.text(xtext,ytext,varis)
            xtext=xtext-1    
        programname='teal.py, tealclass.py, data.py   '+localtime
        param1='\n   input files= '+str(pass_data.fnamec)+'    '    +str(pass_data.fnameb)+'    '+str(pass_data.fnamem) +'    '+str(pass_data.fnamebtextbxy) + '     dt='+str(pass_data.dt)
        start=App.displayinput(pass_data.z[0],75)
        finish=App.displayinput(pass_data.z[-1],75)
        param2='\nstart=  ' + start + '\nfinish=  ' + finish
        titlelsl=programname+param1 + param2
        plt.title(titlelsl, fontsize=8)
        plt.show(block=False) #IMPORTANT: to SHOW graph but NOT stop execution
      
        
    #rounds numbers for x(start), x(final) in the title of plot x(i) vs. time
    def displayinput(vector1,number):
        #creates string to print from np.array(vector1)
        #that is approximately number characters per line
        c=''
        v1=vector1.tolist()
        v2=[round(v1[i],6) for i in range (len(v1))]
        a=str(v2)
        a2=a.replace(' ','')
        a3=list(a2)
        a3[0],a3[-1]='',''
        numend=0
        for i in range(0,len(a3)):
            if (a3[i]==',' and numend >= number):
                numend=0
                a3[i]=',\n'
            numend=numend+1
        c=''.join(a3)
        c2=c.replace(',',',  ')
        return c2

    
    #clear and refresh ONLY the left initial condition dataframe
    def refreshDataFrame(self):
        self.fixent=1 #UGLY FIX FOR ENTRIES/ENTRIESIJ
        App.ClearFrame(self.framed1)
        #frame and buttons on top
        newframe=tk.Frame(self.framed1)
        newframe.pack(side=tk.TOP,pady=0)
        tk.Label(newframe,text='initial conditions',fg='blue').pack(side=tk.LEFT,padx=30,pady=5)
        tk.Button(newframe,text='original',command= self.resetIC).pack(side=tk.RIGHT,padx=30,pady=5)
        newframe2=tk.Frame(self.framed1)
        newframe2.pack(side=tk.TOP,pady=0)
        cal1=tk.Button(newframe2,text='CALCULATE',command=(lambda: self.recalculate(data)))
        cal1.pack(side=tk.LEFT,padx=30,pady=5)
        tk.Button(newframe2,text='ENTER',command=self.refreshPicFrame).pack(side=tk.LEFT,padx=30,pady=5)      
        #frame for entry widgets for initial conditions
        self.framecanvas=tk.Frame(self.framed1)
        self.framecanvas.pack(side=tk.BOTTOM,pady=0)
        #adding the scroll bar
        sizescroll=31*data.numc
        self.canvas = tk.Canvas(self.framecanvas,width=400,height=800,scrollregion=(0,0,sizescroll,sizescroll)) #FROM LAUNY
        self.canvas.pack(side=tk.LEFT)
        scrollbar = tk.Scrollbar(self.framecanvas, command=self.canvas.yview)
        scrollbar.pack(side=tk.LEFT, fill='y')
        self.canvas.config(width=280,height=800)
        self.canvas.configure(yscrollcommand = scrollbar.set)
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')
        # creating the initial condition entry widgets     
        fields=data.labels
        default=[str(i) for i in range(len(data.labels))]
        entries = []
        self.data.zround=[str(round(self.data.z[-1,i],6)) for i in range(len(self.data.z[0]))]                                                           
        for field in fields:
            row = tk.Frame(self.frame)
            lab = tk.Label(row, width=12, text=field, anchor='w')
            ent = tk.Entry(row,width=10)
            row.pack(side=tk.TOP, padx=5, pady=0, expand=1)
            lab.pack(side=tk.LEFT,expand=1)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.Y)
            ent.insert(10,self.data.zround[fields.index(field)])
            entries.append((field, ent))
            self.entries=entries
        #TRANSFORM ALL ENTRIES INTO STARTING VALUES FOR COMPUTATION
        self.data.z[0]=[eval((entries[i][1].get())) for i in range(len(entries))]
        self.outsideframed1.pack(expand=1)  #KEEPING THIS FOR THE MOMENT HERE
        return
        
    
    #redraw the textboxes and the arrows connecting them
    def refreshPicFrame(self):
        #UGLY FIX FOR ENTRIES/ENTRIESIJ----------------------------------------
        if self.fixent==1:
            self.data.z[0]=[eval((self.entries[i][1].get())) for i in range(len(self.entries))]
        if self.fixent==2:
            column=[eval((self.entriesIJ[i][1].get())) for i in range(len(self.entriesIJ))]
            self.data.ca[:,self.box_id]=column
        #UGLY FIX FOR ENTRIES/ENTRIESIJ----------------------------------------        
        #scale b's from z[0] - NOT Z[-1] like in A NEW CALCULATION
        vector=data.z[0]
        self.data.b=App.scalebox(vector)
        #set z[0]=z[-1] for the NEXT iteration
        App.ClearFrame(self.framepic)  
        self.canvas=tk.Canvas(self.framepic,width=800, height=2400)
        f=self.createBoxGraph()
        self.canvas = FigureCanvasTkAgg(f, master=self.framepic)
        self.canvas.show()
        self.canvas._tkcanvas.pack()
        cid=f.canvas.mpl_connect('button_press_event',self.onclick)
        
    
    #clear and refresh ONLY the left cij adjacency matrix dataframe
    def refreshCIJFrame(self):
        self.fixent=2 #UGLY FIX FOR ENTRIES/ENTRIESIJ
        App.ClearFrame(self.framed1)
        fromto='FROM    '+data.labels[self.box_id]+'    TO'
        #frame and top buttons
        newframe=tk.Frame(self.framed1)
        newframe.pack(side=tk.TOP,pady=0)
        tk.Label(newframe,text=fromto,bg='thistle1',fg='red').pack(side=tk.LEFT,padx=5)
        tk.Button(newframe,text='ALL Cij',command= self.FullrefreshPicFrame).pack(side=tk.LEFT,padx=5)
        tk.Button(newframe,text='IC',command= self.refreshDataFrame).pack(side=tk.LEFT,padx=5)
        newframe2=tk.Frame(self.framed1)
        newframe2.pack(side=tk.TOP,pady=0)
        cal2=tk.Button(newframe2,text='CALCULATE',command=(lambda: self.recalculate(data)))
        cal2.pack(side=tk.LEFT,padx=30,pady=5)
        tk.Button(newframe2,text='ENTER',command=self.refreshPicFrame).pack(side=tk.LEFT,padx=30,pady=5)  
        #frame for entry widgets for cij adjacency matrix
        self.framecanvas=tk.Frame(self.framed1)
        self.framecanvas.pack(side=tk.BOTTOM,pady=0)
        #adding the scroll bar
        sizescroll=31*data.numc
        self.canvas = tk.Canvas(self.framecanvas,width=400,height=800,scrollregion=(0,0,sizescroll,sizescroll)) #FROM LAUNY
        self.canvas.pack(side=tk.LEFT)
        scrollbar = tk.Scrollbar(self.framecanvas, command=self.canvas.yview)
        scrollbar.pack(side=tk.LEFT, fill='y')
        self.canvas.config(width=280,height=800)
        self.canvas.configure(yscrollcommand = scrollbar.set)
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')
        # creating the cij adjacency matrix entry widgets
        fields=self.data.labels
        entriesIJ = []                                                         
        for field in fields:
            row = tk.Frame(self.frame)
            lab = tk.Label(row, width=15, text=field, anchor='w',bg='thistle1')
            entIJ = tk.Entry(row,bg='thistle1')
            row.pack(side=tk.TOP, padx=5, pady=1, expand=1)
            lab.pack(side=tk.LEFT,expand=1)
            entIJ.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.Y)
            entIJ.insert(10,self.data.ca[fields.index(field)][self.box_id])
            entriesIJ.append((field, entIJ))
            self.entriesIJ=entriesIJ
        #TRANSFORM ALL ENTRIES INTO STARTING VALUES FOR COMPUTATION
        column=[eval((self.entriesIJ[i][1].get())) for i in range(len(self.entriesIJ))]
        self.data.ca[:,self.box_id]=column
        self.outsideframed1.pack(expand=1)
        return


    #return the textbox id that was clicked
    def onclick(self,event):
        for box in TextBox.list_box:
            contains, attrd = box.text.contains(event)
            if(contains):
                id=box.id
                print('\nid,bname(id)=  ',id, data.labels[id])
                # print('box_%d'  % id)
                # print('box_' + data.bname[id])
                # print('show vars ')
                # self.update_dataFrame(id)
                self.box_id=id
                self.fewarrows=1
                self.refreshCIJFrame()
                # TextBox.selected_box_id=id
                return;
                
    
    #reset the initial conditions to the input data ic(i) default values
    def resetIC(self):
        self.data.z[-1]=[self.data.ica[i] for i in range(len(self.data.z[0]))]
        self.refreshDataFrame()
    
    
    #not used
    def FullrefreshPicFrame(self):
        self.fewarrows=0
        self.refreshPicFrame()
    
    
    #not used, but nice to have to end execution
    def myquit(self):
        print ('\n I did press CLOSE!')
        self.root.destroy()
        
    
    #removes ALL widgets in frame
    #seemed a better option than forget
    def ClearFrame(frame):
        for widget in frame.winfo_children():
            widget.destroy()
        # frame.pack_forget()
        
    
    #not used
    #thought needed for binding scroll bar, apparently not
    def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
#         self.canvas=canvas
        canvas.configure(scrollregion=canvas.bbox('all'))
        
        