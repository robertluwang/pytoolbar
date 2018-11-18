# pytoolbar
# a python toolbar demo in Tkinter
# by Robert Wang
# https://github.com/robertluwang
# Oct-21-2017

try:
# Python2
       import Tkinter as tk
except ImportError:
# Python3
       import tkinter as tk

import webbrowser
import sys, os, time
import win32api

class Login(tk.Toplevel):

    def __init__(self,parent=None):
        tk.Toplevel.__init__(self,parent)
        self.parent=parent
        self.failures = []
        self.failure_max = 3
        self.passwords = [('pytoolbar', 'demo'),('test','test')]
        self.user = tk.StringVar() 
        self.password = tk.StringVar() 
        self.login()
    
    def make_entry(self, parent, caption, width=None, **options):
        tk.Label(self.parent, text=caption).pack(side=tk.TOP)
        entry = tk.Entry(self.parent, **options)
        if width:
                entry.config(width=width)
                entry.pack(side=tk.TOP, padx=10, fill=tk.BOTH)
                return entry
    
    def enter(self,event):
        self.check_password()

    def check_password(self):
        if (self.user.get(), self.password.get()) in self.passwords:
                self.parent.destroy()
                print('Logged in')
                return
        self.failures.append(1)
        if sum(self.failures) >= self.failure_max:
                self.parent.destroy()
                raise SystemExit('Unauthorized login attempt')
        else:
                self.parent.title('Try again. Attempt %i/%i' % (sum(self.failures)+1, self.failure_max))

    def login(self):
        self.parent.geometry('300x160')
        self.parent.wm_attributes("-topmost", 1)
        self.parent.wm_attributes("-toolwindow",1)
        self.parent.protocol('WM_DELETE_WINDOW', self.quitall)
        #entrys with not shown text
        self.user = self.make_entry(self.parent, "User name:", 16, show='*')
        self.password = self.make_entry(self.parent, "Password:", 16, show="*")
        #button to attempt to login
        b = tk.Button(self.parent, borderwidth=4, text="Login", width=10, pady=6, command=self.check_password)
        b.pack(side=tk.BOTTOM)
        self.password.bind('<Return>', self.enter)
        self.user.focus_set()
        self.parent.mainloop()

    def quitall(self):
        root.destroy()
        sys.exit(0)

class Timer(tk.Label):
        def __init__(self,parent=None):
                tk.Label.__init__(self, parent)
                # Simple status flag
                # False mean the timer is not running
                # True means the timer is running (counting)
                self.state = False

                # Our time structure [min, sec, centsec]
                self.timer = [0, 0, 0]
                # The format is padding all the 
                self.pattern = '{0:02d}:{1:02d}:{2:02d}'
                self.button(parent)
                self.update_timeText()
                
        def button(self,parent):
                StartButton = tk.Button(parent, text='S', command=self.start) 
                PauseButton = tk.Button(parent, text='P', command=self.pause)
                ResetButton = tk.Button(parent, text='R', command=self.reset)
        
                StartButton.pack(side=tk.LEFT)
                PauseButton.pack(side=tk.LEFT)
                ResetButton.pack(side=tk.LEFT)
        
        def update_timeText(self):
                if (self.state):

                        # Every time this function is called, 
                        # we will increment 1 centisecond (1/100 of a second)
                        self.timer[2] += 1

                        # Every 100 centisecond is equal to 1 second
                        if (self.timer[2] >= 100):
                                self.timer[2] = 0
                                self.timer[1] += 1
                        # Every 60 seconds is equal to 1 min
                        if (self.timer[1] >= 60):
                                self.timer[0] += 1
                                self.timer[1] = 0
                        # We create our time string here
                        timeString = self.pattern.format(self.timer[0], self.timer[1], self.timer[2])
                        # Update the timeText Label box with the current time
                        self.config(text=timeString)
                # Call the update_timeText() function after 1 centisecond
                self.after(10, self.update_timeText)

        # To start the kitchen timer
        def start(self):
                self.state = True

        # To pause the kitchen timer
        def pause(self):
                self.state = False

        # To reset the timer to 00:00:00
        def reset(self):
                self.timer = [0, 0, 0]
                self.config(text='00:00:00')

class Clock(tk.Label):
    """ Class that contains the clock widget and clock refresh """

    def __init__(self, parent=None):
        tk.Label.__init__(self, parent)
        """
        Create and place the clock widget into the parent element
        It's an ordinary Label element.
        """
        self.time = time.strftime('%H:%M:%S')
        self.configure(text=self.time)
        self.after(200, self.tick)


    def tick(self):
        """ Update the display clock every 200 milliseconds """
        new_time = time.strftime('%H:%M:%S')
        if new_time != self.time:
            self.time = new_time
            self.config(text=self.time)
        self.after(200, self.tick)

class Myaltsearch(tk.Frame):
    def __init__(self,parent=None):
        tk.Frame.__init__(self,parent)
        self.OPTIONS=["google","github","oxford","bab.la","wiki"]
        self.var = tk.StringVar() 
        self.searchtext = tk.StringVar()
        self.myaltsearch(self)

    def myaltsearch(self, parent):
        self.var.set(self.OPTIONS[0])
        apply(tk.OptionMenu, (parent, self.var) + tuple(self.OPTIONS)).pack(side=tk.LEFT)
        tk.Entry(parent,textvariable=self.searchtext,bd=1,width=100).pack(side=tk.LEFT,fill=tk.X, expand=1)
        tk.Button(parent, text="C",command=self.clean).pack(side=tk.LEFT)
        tk.Button(parent, text="Go",command=self.go).pack(side=tk.LEFT)
        
    def go(self):
        stext=(self.searchtext.get()).encode(encoding='UTF-8',errors='strict')
        stext=' '.join(stext.split())
        stext=stext.strip()
        print stext
        if self.var.get() == "google":
                webbrowser.open_new_tab('https://www.google.ca/search?q=%s' % stext)
        elif self.var.get() == "github":
                webbrowser.open_new_tab('https://github.com/search?q=%s' % stext)
        elif self.var.get() == "oxford":
                webbrowser.open_new_tab('https://en.oxforddictionaries.com/definition/%s' % stext)
        elif self.var.get() == "bab.la":
                webbrowser.open_new_tab('http://en.bab.la/dictionary/english-chinese/%s' % stext )
        elif self.var.get() == "wiki":
                webbrowser.open_new_tab('http://en.wikipedia.org/wiki/%s' % stext )

    def clean(self):
        self.searchtext.set('')

class Tool(tk.Frame):
    def __init__(self,parent=None):
        tk.Frame.__init__(self,parent)
        self.tool(self)
            
    def tool(self,parent):
        tk.Button(parent, text="qdir",command=self.qdir).pack(side=tk.LEFT)
        tk.Button(parent, text="git",command=self.git).pack(side=tk.LEFT)
        tk.Button(parent, text="kitty",command=self.kitty).pack(side=tk.LEFT)
        tk.Button(parent, text="scite",command=self.scite).pack(side=tk.LEFT)
 
    def qdir(self):
        win32api.WinExec(curdriver()+'\oldhorse\portableapps\qdir\Q-Dir.exe')
        
    def git(self):
        win32api.WinExec(curdriver()+'\oldhorse\portableapps\git\git-bash.exe')
        
    def kitty(self):
        win32api.WinExec(curdriver()+'\oldhorse\portableapps\kitty\kitty_portable.exe')
        
    def scite(self):
        win32api.WinExec(curdriver()+'\oldhorse\portableapps\scite\SciTE.exe')
              
class Link(tk.Frame):
    def __init__(self,parent=None):
        tk.Frame.__init__(self,parent)
        self.link(self)
        
    def link(self,parent):
        tk.Button(parent, text="blog",command=self.blog).pack(side=tk.LEFT) 
        tk.Button(parent, text="github",command=self.github).pack(side=tk.LEFT) 
        tk.Button(parent, text="facebook",command=self.facebook).pack(side=tk.LEFT)	
        
    def blog(self):
        webbrowser.open_new_tab('http://dreamcloud.artark.ca/')
        
    def github(self):
        webbrowser.open_new_tab('https://github.com/robertluwang')
        
    def facebook(self):
        webbrowser.open_new_tab('https://www.facebook.com/robert.wang.58')
    
class Topmenu(tk.Menu):
    def __init__(self,parent=None):
        tk.Menu.__init__(self,parent)
        self.parent=parent
        self.topmenu()

    def topmenu(self):
        self.menubar = tk.Menu(self.parent)
        self.filemenu = tk.Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(label="Exit",command=self.parent.destroy)	
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.parent.config(menu=self.menubar)
        
def curdriver():
    return os.getcwd().split(":")[0]+":"
    
    
if __name__ == "__main__":

        root = tk.Tk() 
        root.title('Welcome to pytoolbar 1.0')
        login1 = Login(root)
        
        root = tk.Tk() 
        root.resizable(0,0)
        root.title('pytoolbar 1.0')
        root.wm_attributes("-topmost", 1)
        root.wm_attributes("-alpha",0.9)
        
        topmenu1 = Topmenu(root)
        
        frame1  = tk.Frame(root)
        frame1.grid(row=0)
        frame2  = tk.Frame(root)
        frame2.grid(row=1)
        frame3  = tk.Frame(root)
        frame3.grid(row=2)
        
        #frame1
        clock1 = Clock(frame1)
        clock1.configure(font=('Helvetica', 10), bg='grey')
        clock1.pack(side=tk.LEFT)
        
        tk.Label(frame1, text="pytoolbar",width=60,font=('Helvetica', 10)).pack(side=tk.LEFT)
        
        timer1 = Timer(frame1)
        timer1.configure(text="00:00:00", font=("Helvetica", 10), bg='grey')
        
        timer1.pack(side=tk.LEFT)
        
        # frame2
        myaltsearch1 = Myaltsearch(frame2)
        myaltsearch1.pack(side=tk.LEFT)
        
        #frame3
        tool1 = Tool(frame3)
        tool1.pack(side=tk.LEFT)
        link1 = Link(frame3)
        link1.pack(side=tk.LEFT)
        
        
        
        
        root.mainloop()
