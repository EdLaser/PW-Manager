#------------Imports------------#
import os.path           #add functions for path names
import csv               #work with csv files
import PySimpleGUI as ui #GUI 
import hashlib           # to Encode passwords
import string            #to define Password characters
from random import *     #generate random passwords

#global variables
log = 0         #check for first opening of user
hash_pw = ""    #PW to write in Data for Login
pw_read = ""    #Global PW for Login
pw_dict = {}    #Dictionary for Entrys
keys = []       #Keys of Dict (Websites) for Identification
#------------Functions------------#
#loading bar ( for optics)
def loading_bar():
    #configure the layout
    layout = [
        [ui.Text("loading...")],                                           #Textfield to show that loading is in progress
        [ui.ProgressBar(100, orientation='h', size=(20,20), key='-prog-')] #progressbar that shows actuall progress
    ]
    #create the window
    window = ui.Window("Starting..",layout)
    prog_bar = window['-prog-']                                             #make prog bar updatable
    for i in range(100):                                                    #update from 1 to 100
        event,values = window.read(timeout=1)                               #read the events with 1 ms timeout
        if event == ui.WIN_CLOSED:                                          #break if window is closed
            break
        prog_bar.UpdateBar(i + 1)                                           #update the bar with little steps
    window.close()                                                          #close window at the end

#generate new random password
def generate_password():
                #String 0123456789  #String upper and lower case letters    #string of all ascii characters
    characters = string.digits + string.ascii_letters + string.punctuation  #all strings joined together
    password = "".join(choice(characters) for x in range(14))               #randomly join the strings together to get a random password
    
    if ui.PopupYesNo("Set as new Password?", password, font = ("AppleGothic",12)) == "Yes": #popup to set the password 
        return password #return it 
    else:
        return  #do nothing if password is declined

#Check for file in path of code
def check_file(file_name): 
    if os.path.exists(file_name): #if path refers to existing path
        return 1 # do nothing if file exists
    else: #create File
        file = open(file_name, 'w')# if file does not exists create it for writing
        file.close() #close the file
    return 0 #return 0 for failure      

#read from file
def read_string_fromfile(file_name):
    #read  the string from .user.txt
    with open(file_name) as file:
        string_read = file.read() #read it in
    return string_read #return the string

#write passwords to file
def write_password(web,user,pw):
    with open(".passwords.txt",'a') as write_file: #open file to append a row
        writeable = [web,user,pw] #create the writable string with passed parameters
        writer = csv.writer(write_file, delimiter= ';') #setup csv writer
        writer.writerow(writeable) #write the row of data with csv writer

#read passwords
def read_all_passwords():
    #treat file operation as whole statement to ease file handling
    global pw_dict #refer to global pw dictionary
    pw_dict = {}   #create it empty
    with open(".passwords.txt",'r') as read_file: #open file for reading
        reader = csv.reader(read_file, delimiter=';') #setup csv reader
        for row in reader: #read all rows into dictionary with lists
            pw_dict[row[0]] = [row[1], row[2]] #row 0 is the key, row 1 and row 2 are a value pair as a List
        global keys #refer to global key variable
        keys = pw_dict.keys() #get all keys of dictionary

#Enter a Website refered to
def enter_website():
    #create the layout (popup window was not quite suitable here)
    layout = [
        [ui.Text("Enter Website", font = ('AppleGothic',12))],                                      #Textfield above input field
        [ui.InputText(size =(12,1), key = "-WEB-", do_not_clear=False, font = ('AppleGothic',12))], #InputField for the website 
        [ui.Button("OK", font = ('AppleGothic',12)),ui.B("Cancel", font = ('AppleGothic',12))],     #Buttons to confirm or cancel
    ]
    #create the windows
    window = ui.Window("Test ", layout)
    #read the window
    event, values = window()
    if event == "Cancel" or event == ui.WIN_CLOSED:           #if cancel is pressed or window is closed return none
        window.close()
        return "none"
    if event == "OK":                                         #if confirmed return the entered value
        window.close()
        return values["-WEB-"]

#search for single password
def search_password():
    search = ""                         #create empty search string 
    while search not in keys:           #as long as search isnt in dictionary keys
        search = enter_website()        #call enter_website fct
        if search == "none":            #If canceled return 0 for failure
                return 0
        if search in keys:              #If website is found
            return search  
        else:                           #Website not found
            ui.popup_error("Website not featured!", keep_on_top=True, font = ('AppleGothic',12)) #Error popup

#add PAssword to list
def add_password(): 
    #create empty strings for website,password and username
    web = ""
    user = ""
    pw = ""
    #create the layout
    layout = [
            [ui.Text("Website", font = ('AppleGothic',12))],                                #Textfield above Website Input
            [ui.InputText(key="-WEBSITE-",do_not_clear=True, font = ('AppleGothic',12))],   #Website Input
            [ui.Text("Username", font = ('AppleGothic',12))],                               #text above username input
            [ui.InputText(key="-USERNAME-",do_not_clear=True, font = ('AppleGothic',12))],  #username input
            [ui.Text("Password", font = ('AppleGothic',12))],                               #text above password input
            [ui.InputText(key="-PASSWORD-",do_not_clear=True, font = ('AppleGothic',12))],  #username input
            #Button Panel to confirm, cancel or add a random password
            [ui.B("Confirm",bind_return_key=True, font = ('AppleGothic',12)),ui.B("Cancel", font = ('AppleGothic',12)), ui.B("Random PW", font = ('AppleGothic',12), key="-RANDOM-"),ui.B("Clear", font = ('AppleGothic',12), key="-CLEAR-")]
        ]
    #build window with layout
    window = ui.Window("New Password",layout)
    #Event read loop    
    while True:
        event, values = window.read()                       #read the window
        if event == 'Cancel' or event == ui.WIN_CLOSED:     #if cancel is clicked or window is closed return 0 and close window
            window.close()
            return 0
        else:               
            if event == "Confirm":                          #if confirm is pressed
                if  not values["-WEBSITE-"] or not values["-USERNAME-"] or not values ["-PASSWORD-"]:               #check if inputs arent empty
                    ui.popup_error("Please fill in all values",keep_on_top=True, font = ('AppleGothic',12))         #if empty popup_error to remind to fullfill 
                    continue                                                                                        #continue to read values from user input
                else:
                    if ui.popup_yes_no("Set password ?",keep_on_top=True, font = ('AppleGothic',12)) == "Yes":      #pop for confirmation if password should be set
                        web = values["-WEBSITE-"]          #asign values of inputs to variables
                        user = values["-USERNAME-"]        #-"-
                        pw = values ["-PASSWORD-"]         #-"-
                        write_password(web,user,pw)        #write the password into the file
                        ui.popup("Success!", auto_close=True, auto_close_duration=0.75, font = ('AppleGothic',12))  #popup to confirm success
                        read_all_passwords()               #refresh pw_dict with new values
                        continue #continue adding passwords
                    else:
                        return 0 #Failed
            if event == "-RANDOM-":               #if user wants random password
                pw = generate_password()          #asign random password to pw variable
                window["-PASSWORD-"].update(pw)   #update password-input with generated password
            if event =="-CLEAR-":                 #if clear is clicked empty the inputs
                    window["-WEBSITE-"].update("")
                    window["-USERNAME-"].update("")
                    window["-PASSWORD-"].update("")

#delete Password
def delete_password():
    #refresh dictionary
    read_all_passwords()
    elements = list(keys)   #get dict keys as list
    #create the checkbox
    box = [
        [ui.Listbox(values=elements, select_mode = ui.LISTBOX_SELECT_MODE_SINGLE, size=(30,len(elements)), bind_return_key=True, font = ('AppleGothic', 12), key = "-BOX-")],
        [ui.B("Cancel")]
    ]
    #create Window
    window = ui.Window("Delete a password", box)
    #event loop
    while True:
        event, values = window.read()
        if event =="Cancel" or event == ui.WIN_CLOSED:  #cancel is pressed or window is closed
            window.close()
            return 0                                    #return 0 as closed
        else:
            result = str(values["-BOX-"][0])            #Convert the result ( list ) into a string
            if ui.PopupYesNo("Delete Password ?", result) == "Yes":
                #overwrite all except searched tupel
                updated_list = [] #create the updated list after delition
                with open(".passwords.txt") as read_file:                 #open the password file
                    reader = csv.reader(read_file, delimiter= ';')        #setup the reader
                    for x in reader:                                      #loop thrue all read rows
                        if x[0]!= result:                                 #as long as the website is not the searched website
                            updated_list.append(x)                        #append the tupel to the updated list
                    with open(".passwords.txt",'w') as write_file:        #open file to write the password
                        writer = csv.writer(write_file, delimiter= ';')   #setup writer
                        writer.writerows(updated_list)                    #write the updated list into the file
                window.close()
                return 1
            else:       #do nothing if no is pressed
                pass

#Check if a user is already present (for logging in manager)
def check_user():
    #check if user file is already present and is not empty(a password is writen)
    if check_file(".user.txt") and os.stat(".user.txt").st_size!=0:
        global pw_read                              #refer to global password for login
        pw_read = read_string_fromfile(".user.txt") #read in th user password
    else:#if password is not writen/file is corrupted
        #setup layout for first login
        layout = [
            [ui.Text("Set Password", font = ('AppleGothic',12))],                           #Texfield above password input
            [ui.InputText(key="-PWFIRST-",do_not_clear=False, font = ('AppleGothic',12))],  #First password input
            [ui.Text("Confirm Paswword", font = ('AppleGothic',12))],                       #Text above password confirmation
            [ui.InputText(key="-PWSECOND-",do_not_clear=False, font = ('AppleGothic',12))], #Input of password confirmaton
            #button panel for confirmation, cancel, clearing or to add random password
            [ui.B("Confirm",bind_return_key=True, font = ('AppleGothic',12)),ui.B("Cancel", font = ('AppleGothic',12)), ui.B("Random PW", font = ('AppleGothic',12), key="-RANDOM-"),ui.B("Clear", font = ('AppleGothic',12), key="-CLEAR-")]
        ]
        #Create window
        window = ui.Window("New user",layout)
        #event loop
        while True:
            event,values = window.read()                    #read from the window
            if event == 'Cancel' or event == ui.WIN_CLOSED: #if window is closed or cancel is pressed
                break                                       #break the loop
            else:                                           
                if event == "Confirm":                      #if confirm has been pressed
                    pw_first = values["-PWFIRST-"]          #asign pwFirst with input values
                    pw_second = values ["-PWSECOND-"]       #asign pwSecond with input values
                    if not pw_first or not pw_second:
                        ui.popup_error("Please fill in all values",keep_on_top=True, font = ('AppleGothic',12))         #if empty popup_error to remind to fullfill
                        continue
                    else:
                        if pw_first == pw_second:               #check if passwords match
                            ui.popup("Success, Password set", auto_close=True, auto_close_duration=0.75, keep_on_top=True)  #pop for success
                            window.close()                      #close the window
                        else:
                            ui.popup_error("Passwords don't match", font = ('AppleGothic',12))  #popup, error occured
                if event =="-RANDOM-":                      #if user wants random password
                    random = generate_password()            #generate a password and asign to random
                    window["-PWFIRST-"].update(random)      #set generated passord to inputs
                    window["-PWSECOND-"].update(random)
                if event =="-CLEAR-":                       #if clear is clicked empty the inputs
                    window["-PWFIRST-"].update("")
                    window["-PWSECOND-"].update("")
                    
        #Convert PW to hash
        global hash_pw   #refer to gloal password hash (string)
        hash_pw = hashlib.md5(pw_first.encode('utf-8')) #asign hash of first password to hash_pw string
        with open(".user.txt", 'w') as writer:         #write pw hash to file
            writer.write(hashPW.hexdigest())           #write a string of the password hash into the file
            writer.close()
        global log                                     #Set log to 1 to see that pw has been writen first time
        log = 1
    return 1                                           #return 1 (success)

#Login Window
def login():
        #check if passwords file exists
        check_file(".passwords.txt")
        #create the layout
        layout = [
            #login field with seperator between input and textfield
            [ui.Text("Enter Password",font = ('AppleGothic',14)),ui.VerticalSeparator(),ui.InputText(size= (25,2) ,key="-PWINPUT-",do_not_clear=False,font = ('AppleGothic',12))],
            #button panel
            [ui.B("Confirm",bind_return_key=True,auto_size_button=True, font = ('AppleGothic',12)),ui.B("Cancel", font = ('AppleGothic',12))]
        ]
        #build the window
        window = ui.Window("Login", layout,size=(250,100))
        #event loop
        while True:
            event,values = window.read()
            if event == 'Cancel' or event == ui.WIN_CLOSED:     #if window is closed or cancel is pressed
                return 0                                        # 0 to End programm
            else:
                if event == "Confirm":                          #if confirm is pressed
                    loading_bar()                               #display loading bar
                    entered_pw = hashlib.md5(values["-PWINPUT-"].encode('utf-8')) #encode entered password as hash value
                    #log == 0 -> program has been opened before
                    if log == 0:
                        if pw_read == entered_pw.hexdigest():                     #Compare compare the hash strings of read and typed password
                            #strings match -> entered password is correct
                            ui.popup("Login Succesfull",keep_on_top=True, auto_close=True, auto_close_duration=0.75, font = ('AppleGothic',12)) #auto closed after 0.75 seconds
                            window.close()  #close login window
                            return 1        #return 1 for success
                        else:               #something went wrong
                            #login failed -> show error
                            ui.popup_error("Login failed, check data and try again",keep_on_top=True, font = ('AppleGothic',12)) 
                    #log == 1 -> A new user password has been set
                    if log == 1:
                        if hash_pw.hexdigest() == entered_pw.hexdigest():   #compare entered password and set password in check_user
                            ui.popup("Login Succesfull",keep_on_top=True, auto_close=True, auto_close_duration=0.75, font = ('AppleGothic',12)) #popip for success
                            return 1
                            window.close()  #close the window
                        else:
                            ui.popup_error("Login failed, check data and try again",keep_on_top=True, font = ('AppleGothic',12))    #error popup

#Funktion To print results
def print_result(res,window): #call with a key and a window
    data = pw_dict[res]       #res as key for pw dictionary
    window["-OUT-"].print(res +" : \t\t\tUsername: " + data[0] + "\t\t\tPassword: " + data[1])  #print key with data pair

# Main Programm overlay
def mainframe():
    #read from file into dictionary
    read_all_passwords()
    #set layout of overlay
    layout = [
        [ui.B("Show all Passwords", key="-ALLPW-", font = ('AppleGothic',12)),  #button to print passwords
         ui.B("Search for Password",key="-SEARPW-", font = ('AppleGothic',12)), #button to search for password and print it
         ui.B("Add Password",key="-ADDPW-", font = ('AppleGothic',12)),         #button to add a password
         ui.B("Delete Password",key="-DELPW-", font = ('AppleGothic',12)),      #button to delete a featured password
         ui.B("EXIT", font = ('AppleGothic',12))],                              #button to exit program
        [ui.HorizontalSeparator()],                                             #add a seperator
        [ui.Multiline(size=(70,30),key="-OUT-",do_not_clear=False,font=('AppleGothic', 14))]    #multiline to print results
    ]
    #create window
    window = ui.Window("Manager", layout)
    #event loop
    while True:
            #read window
            event,values = window.read()
            if event == "EXIT" or event == ui.WIN_CLOSED:     #if window is closed or cancel is pressed
                break                                         #break loop
            if event == "-ALLPW-":                      #if all passwords are searched
                read_all_passwords()                    #update the dictionary
                for x in keys:                          #print loop fr all keys
                    print_result(x,window)              #print key and value pair
            if event == "-SEARPW-":                         #Search PW Button pressed
                result_sear = search_password()             #asign search result to result
                if result_sear == 0:                        #if the search is canceled or a failure occured
                    continue                                #continue the loop
                else:
                    print_result(result_sear,window)        #print the result of the search
            if event =="-ADDPW-":                       #Add PW Button pressed
                result_add = add_password()             #asign result of add_password to result_add
                if result_add == 0:                     #if adding is canceled continure
                    continue   
            if event =="-DELPW-":                       #if delete is pressed
                result_del = delete_password()          #asign result of delete_password to result_del
                read_all_passwords()                    #refresh the dictionary
                if result_del == 1:
                    for x in keys:                      #print loop fr all keys
                        print_result(x,window)          #print key and value pair
                if result_del == 0:                     #if deletion is canceled continue
                    continue

#------------Main------------#
ui.theme('DefaultNoMoreNagging') #add a theme for beautification
loading_bar()                    #display the loading bar 
check_user()                     #check if a user is registered
if login() == 1:                 #if login is successfull
    mainframe()                  #grant acces to mainframe
else:
    exit()                       #otherwise exit