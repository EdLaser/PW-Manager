#------------Imports------------#
import os.path #add functions for path names
import csv     #work with csv lists
import PySimpleGUI as ui#GUI 
import hashlib # to Encode passwords

#global variables
log = 0         #check for first opening of user
hashPW = ""     #PW to write in Data for Login
pw_read = ""    #Global PW for Login
pw_list = {}    #Dictionary for Entrys
keys = []       #Keys of Dict (Websites) for Identification
search = ""     #Website searched for 

#------------Functions------------#
#Check for file in path of code
def check_file(file_name):
    if os.path.exists(file_name): #if path refers to existing path
        return 1 # do nothing if file exists
    else: #create File
        file = open(file_name, 'w')# if file does not exists create it for writing
        file.close()
    return 0       

#read from file
def read_string_fromfile(file_name):
    with open(file_name) as file:
        string_read = file.read()
    return string_read

#read passwords
def read_all_passwords():
    #treat file operation as whole statement to ease file handling
    global pw_list
    with open("passwords.txt",'r') as read_file: #open file for reading
        reader = csv.reader(read_file, delimiter=';') #setup reader
        for row in reader: #read all rows into dictionary with lists
            pw_list[row[0]] = [row[1], row[2]]
        global keys
        keys = pw_list.keys()

#search for single password
def search_password():
    global search
    search = ""
    while search not in keys:
        search = ui.popup_get_text("Enter Website", size=(18,1), keep_on_top=True)
        if search == None:
            break
        else:
            ui.popup_error("Website not featured!", keep_on_top=True)
    return search

#write passwords to file
def write_password():
    #get data from user
    website = input("Enter website refered to: ")
    username = hinput("Enter username: ")
    password = input("Password: ")
    writeable =website,username,password
    
    with open("passwords.txt",'a') as write_file: #open file for reading
        writer = csv.writer(write_file, delimiter= ';')#setup writer
        writer.writerow(writeable)
    return 0

#Check if a user is already present
def check_user():
    if check_file(".user.txt") and os.stat(".user.txt").st_size!=0: #. for hidden file
        global pw_read #read in login PW
        pw_read = read_string_fromfile(".user.txt") 
        print(pw_read)
    else:
        layout = [
            [ui.Text("Create user",justification='c')],
            [ui.Text("Set Password")],
            [ui.InputText(key="-PWFIRST-",do_not_clear=False)],
            [ui.Text("Confirm Paswword")],
            [ui.InputText(key="-PWSECOND-",do_not_clear=False)],
            [ui.B("Confirm",bind_return_key=True),ui.B("Cancel")]
        ]
        window = ui.Window("New user",layout)
        #Create window
        while True:
            event,values = window.read()
            if event == 'Cancel' or event == ui.WIN_CLOSED:
                break
            else:
                if event == "Confirm":
                    pwFirst = values["-PWFIRST-"]
                    print(pwFirst)
                    pwSecond = values ["-PWSECOND-"]
                    if pwFirst == pwSecond:
                        ui.popup("Success, Password set")
                        window.close()
                    else:
                        ui.popup_error("Passwords don't match")
        #Convert PW to hash
        global hashPW
        hashPW = hashlib.md5(pwFirst.encode('utf-8'))
        with open(".user.txt", 'w') as read_user:
            read_user.write(hashPW.hexdigest())
            read_user.close()
        global log #Set log to 1 to see that pw has been writen first time
        log = 1
    return 1

#Login Window
def login():
        check_file("passwords.txt")
        layout = [
            [ui.Text("Enter Password"),ui.InputText(size= (15,1) ,key="-PWINPUT-",do_not_clear=False)],
            [ui.B("Confirm",bind_return_key=True),ui.B("Cancel")]
        ]
        window = ui.Window("Login",layout)
        while True:
            event,values = window.read()
            if event == 'Cancel' or event == ui.WIN_CLOSED:
                break
            else:
                if event == "Confirm":
                    passCoded = hashlib.md5(values["-PWINPUT-"].encode('utf-8')) #Entered PW as hash
                    print("Entered:"+ values["-PWINPUT-"])
                    if log == 0:
                        if pw_read == passCoded.hexdigest():                     #Compare entered and read PW
                            ui.popup("Login Succesfull",any_key_closes=True,keep_on_top=True) #closed by every key
                            window.close()
                        else:
                            ui.popup_error("Login failed, check data and try again",any_key_closes=True,keep_on_top=True)
                    if log == 1:                                                #First opening
                        if hashPW.hexdigest() == passCoded.hexdigest():
                            ui.popup("Login Succesfull",keep_on_top=True)
                            window.close()
                        else:
                            ui.popup_error("Login failed, check data and try again",keep_on_top=True)
        return 1

#Main Programm overlay
def mainframe():
    #Interaction Buttons
    button_pannel = [
        [ui.B("Show all Passwords", key="-ALLPW-")],
        [ui.B("Search for Password",key="-SEARPW-")],
        [ui.B("Add Password",key="-ADDPW-")],
        [ui.B("EXIT")]
    ]
    #Textfield for Output
    text_field = [
        [ui.Multiline(size=(40,30),key="-OUT-",do_not_clear=False)]
    ]

    layout = [
        [
            ui.Column(button_pannel),
            ui.VerticalSeparator(),
            ui.Column(text_field),
        ]
    ]
    #Main Window
    window = ui.Window("Manager",layout)
    #read all passwords for backup
    read_all_passwords()
    while True:
            event,values = window.read()
            if event == "EXIT" or event == ui.WIN_CLOSED:
                break
            if event == "-ALLPW-":
                print(keys)
                for x in keys:
                    data = pw_list[x]
                    window["-OUT-"].print(x +":   " + "username: " + data[0] + "   password: " + data[1])
            if event == "-SEARPW-":
                result = search_password()
                data = pw_list[result]
                window["-OUT-"].print(result+":   " + "username: " + data[0] + "   password: " + data[1])


#------------Main------------#
check_user()
login()
mainframe()