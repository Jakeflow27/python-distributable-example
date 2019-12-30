# Imports For python > 3.1
from tkinter import *
from tkinter import ttk
import configparser
import hashlib
from time import sleep

# Globals, parsed from the config file
config = configparser.ConfigParser()
config.read('config.ini')
USER = config['DEFAULT']['api-user']
PASS = config['DEFAULT']['api-pass']

# Setting with default value if null
LOGIN_MESSAGE = config['DEFAULT']['login-message'] or "Please log in"
SUCCESS_MESSAGE = config['DEFAULT']['success-message'] or "Logged in"


def makeRootWidget():
    # Main window
    ws = Tk(className="Demo")
    ws.columnconfigure(0, weight=1)
    ws.rowconfigure(0, weight=1)

    # Input placeholders
    ws.INPUT_USER = StringVar()
    ws.INPUT_PASS = StringVar()

    def login():
        ws.loginFrame.status("") # Clear previous status
        u = ws.INPUT_USER.get()
        p = ws.INPUT_PASS.get()
        if checkUser(u) and checkPass(p):
            print("Logged in")
            ws.contentFrame = makeContentWidget(ws)
            return True
        print("Invalid Credentials")
        ws.loginFrame.status("Invalid Credentials")
        sleep(1)

    ws.login = login

    return ws


def makeContentWidget(parent):
    # Just overwrite the login page
    ws = ttk.Frame(parent, padding=(25, 25, 25, 25))
    ws.grid(column=0, row=0, sticky=N+W+S+E)
    # Success message
    Label(ws, text=SUCCESS_MESSAGE).grid(row=0, columnspan=2)
    ws.columnconfigure(1, weight=1)
    return ws


def makeLoginWidget(parent):

    # Make a flex grid container for the login page
    ws = ttk.Frame(parent, padding=(25, 25, 25, 25))
    ws.grid(column=0, row=0, sticky=N+W+S+E)
    ws.columnconfigure(1, weight=1)

    # Login message
    Label(ws, text=LOGIN_MESSAGE).grid(row=0, columnspan=2)

    # User and Password fields
    Label(ws, text="User Name").grid(row=1, column=0)
    Entry(ws, textvariable=parent.INPUT_USER).grid(
        row=1, column=1, sticky=W+E+N+S, padx=5, pady=5)
    Label(ws, text="Password").grid(row=2, column=0, padx=5, pady=5)
    passEntry = Entry(ws, textvariable=parent.INPUT_PASS, show='*')
    passEntry.grid(row=2, column=1, sticky=W+E+N+S, padx=5, pady=5)

    # Login button
    btn = Button(ws, text='Login', command=parent.login)
    parent.bind('<Return>', lambda event=None: btn.invoke())
    btn.grid(row=3, columnspan=2, sticky=N, pady=10, ipadx=20)

    # Status message
    def status(s):
        Label(ws, text=s, fg="red", font=("Helvetica", 12) ).grid(row=4, column=0, columnspan=2, ipadx=10, ipady=10)

    ws.status = status

    return ws

def hash(s): return hashlib.sha256(s.encode()).hexdigest()

def checkUser(s): return hash(s) == USER

def checkPass(s): return hash(s) == PASS

def main():
    root = makeRootWidget()
    root.loginFrame = makeLoginWidget(root)
    print(root)
    root.mainloop()


main()
