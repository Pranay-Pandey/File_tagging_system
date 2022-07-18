# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 16:45:03 2022

@author: pranay pandey
"""

import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, Text
import json
import re

def add_meta(image, meta):          #not part of the code but is a trial to add tags to the meta data of any file
    with open(image, 'a+b') as f:   #works for image files not any other
        f.write(json.dumps(meta).encode('utf-8'))

def read_meta(image):               #not part of the code but is a trial to get tags from the meta data of any file
    with open(image, 'rb') as f:
        data = str(f.read())
    meta = re.findall(r'xff.*({.*})\'\Z', data)[-1]
    return meta

#dict
tags ={}
files={}
if os.path.isfile('tags.txt'):
    with open('tags.txt','r') as f:
        tempApps = f.read()
        tempApps = tempApps.replace("\'", "\"")
        print(tempApps)
        res = json.loads(tempApps)
        tags = res
if os.path.isfile('files.txt'):
    with open('files.txt','r') as f:
        tempApps = f.read()
        tempApps = tempApps.replace("\'", "\"")
        print(tempApps)
        res = json.loads(tempApps)
        files = res


print(os.getcwd())
def add_tag(dirr=os.getcwd()):          #tags the files recursively to the system
    for entry in os.listdir(dirr):
            rootdir = dirr
            file_path = Path(entry)
            file_loc = os.path.join(rootdir, entry)
            if not os.path.isfile(file_loc):
                add_tag(file_loc)
                continue
            
            print(file_path)
            tag = input('Tags: ').split(' ')
            for k in tag:
                if k in tags:
                    tags[k].append(file_loc)
                else:
                    tags[k] = [file_loc]
                    

def file_tag(file_address,tag):         #tags the file address to the tag 
    if tag!='' and len(tag)!=0:         #in the tag dictionary
        if tag in tags:
            if file_address not in tags[tag]:
                tags[tag].append(file_address)
        else:
            tags[tag] = [file_address]
            
        tag_to_file(file_address, tag)
            
def tag_to_file(file_address,tag):      #in the files dictionary maps file_address
    if tag!='' and len(tag)!=0:         #to tag
        if file_address in files:
            if tag not in files[file_address]:
                files[file_address].append(tag)
        else:
            files[file_address] = [tag]
    
        
        
def remove_tag(file_address,tag):       #removes tag from tags dictionary
    if tag in tags:
        if file_address in tags[tag]:
            tags[tag].remove(file_address)
            if (len(tags[tag])==0):
                k = tags.pop(tag)
            
    remove_file(file_address, tag)      #call for removing from files dictionary
            
def remove_file(file_address,tag):      #removes tag from files dictionary
    if file_address in files:
        if tag in files[file_address]:
            files[file_address].remove(tag)
    if len(tag)==0:
        if file_address in files:
            for i in range(len(files[file_address])):
                remove_tag(file_address, files[file_address][i])
            k = files.pop(file_address)
        
        
def check_file_exists(entry_list):      #checks if file is moved
    for file in entry_list:             #if moved deletes file from files dic
        if not os.path.isfile(file):    #and tags dict
            remove_file(file)
            entry_list.remove(file)
    return entry_list

def get_labels(tag_name,existing_list=[]):      #gets all files for a particular tag
    if (len(existing_list)==0):
        if tag_name[0]=='~':
            tag_to_exclude = tag_name[1:len(tag_name)]
            if tag_to_exclude in tags:
                list_to_return = []
                for tags_to_include in tags:
                    if tags_to_include==tag_to_exclude:
                        continue
                    else:
                        list_to_return = list(set(list_to_return).union(get_labels(tags_to_include)))
                list_to_return = [ element for element in list_to_return if element not in get_labels(tag_to_exclude)] 
                return check_file_exists(list_to_return)
            else:
                return []
        if tag_name in tags:    
            return check_file_exists(tags[tag_name])
        else:
            return []
    
    if tag_name in tags:
        comming_list = tags[tag_name]
        new_list = list(set(existing_list).intersection(comming_list))
        if len(new_list)==0:
            return []
        else:
            return check_file_exists(new_list)
    else:
        if tag_name[0]=='~':
            tag_to_exclude = tag_name[1:len(tag_name)]
            list_to_exculde = get_labels(tag_to_exclude)
            return check_file_exists([element for element in existing_list if element not in list_to_exculde])
        return []
    
        

root = tk.Tk()          #root GUI window
apps = []               #list of to be displayed files/tag

def reset_apps():       #resets apps list
    global apps         #clears the display
    apps = []
    for widget in frame.winfo_children():
        widget.destroy()

def addApp():           #fetch file from explorer
    
    for widget in frame.winfo_children():
        widget.destroy()

    filename =filedialog.askopenfilename(initialdir=os.getcwd(),title="Select file",filetypes=(("all files","*.*"),("executables","*.exe")))
    if len(filename)<1:
        pass
    else:
        apps.append(filename)
        print(filename)
        
    for app in apps:
        label = tk.Label(frame, text=app, bg="gray")
        label.pack()
        
def runApps():          #Runs the indexed file or application from the list of files
    files_to_run = inputtxt.get(1.0, "end-1c").split(' ')
    for i in range(len(files_to_run)):
        num = int(files_to_run[i])
        file_exists = os.path.exists(apps[num-1])
        if file_exists==1:
            os.startfile(apps[num-1])
        else:
            remove_file(apps[num-1], [])
        
def printInput():       #Tags the selected files to the tag(s) from input
    inp = inputtxt.get(1.0, "end-1c").split(' ')
    if inp==['']:
        reset_apps()
        label = tk.Label(frame, text='No files selected to tag', bg="gray")
        label.pack()
        return
    
    else:
        
        if len(apps)!=0:
            yes = 0
            print("apps = ",apps)
            print("tags = ",inp)
            for a in apps:
                for t in inp:
                    file_tag(a,t)
        reset_apps()
        
            
    

def gettaggedfiles():           #get the files associated to a tag
    reset_apps()
    inp = inputtxt.get(1.0, "end-1c").split(' ')
    print(inp)
    files = []
    if (inp!=['']):
        if '/' in inp[0]:
            inputs_broken = inp[0].split('/')
            for k in inputs_broken:
                files = list(set(files).union(get_labels(k)))
        else:
            files = get_labels(inp[0])
        if (len(inp)>1):
            for i in range(1,len(inp)):
                files_prev = []
                if '/' in inp[i]:           #The OR operation
                    inputs_broken = inp[i].split('/')
                    for k in inputs_broken:
                        files_prev = list(set(files_prev).union(get_labels(k)))
                    files = list(set(files).intersection(files_prev))
                else:
                    files = get_labels(inp[i],files)
                
        print(files) 
        if (len(files)==0):
                label = tk.Label(frame, text='No files match', bg="gray")
                label.pack()
        else:
            index = 0
            global apps
            apps = []
            for file in files:
                label = tk.Label(frame, text=str(index+1) +") " +file, bg="gray")
                apps.append(file)
                label.pack()             
                index += 1 
    else:
        label = tk.Label(frame, text="All Tags : ", bg="gray")
        label.pack() 
        for tag in tags:
            label = tk.Label(frame, text=tag, bg="gray")
            label.pack() 
    
        
def getag_for_file():           #Get all the tags associated to a file
    inp = inputtxt.get(1.0, "end-1c").split(' ')
    if len(apps)==0 or inp==['']:
        label = tk.Label(frame, text='No files selected', bg="gray")
        label.pack()
    else:
        inp = int(inp[0])
        index = 1
        file_to_get_tag = apps[inp-1]
        reset_apps()
        apps.append(file_to_get_tag)
        if file_to_get_tag in files:
            for i in range(len(files[file_to_get_tag])):
                tag = files[file_to_get_tag][i]
                label = tk.Label(frame, text=str(index) +") " +tag, bg="gray")
                apps.append(tag)
                label.pack()             
                index += 1 
        else:
            label = tk.Label(frame, text="No tags", bg="gray")
            label.pack()    
        
        '''
        for tag in tags:
            if file_to_get_tag in tags[tag]:
                label = tk.Label(frame, text=str(index) +") " +tag, bg="gray")
                apps.append(tag)
                label.pack()             
                index += 1 
        '''
                
def removetags_for_file():          #removes the particular tag for a particukar file
    inp = inputtxt.get(1.0, "end-1c").split(' ')
    if len(apps)==0:
        reset_apps()
        label = tk.Label(frame, text='No tags selected', bg="gray")
        label.pack()
    else:
        if apps[1] in tags:
            inp_int_len = len(inp)
            for i in range(inp_int_len):
                remove_tag(apps[0], inp[i])
        else:
            label = tk.Label(frame, text='No tags selected', bg="gray")
            label.pack()
    


canvas = tk.Canvas(root, height=450,width = 700, bg = '#263D42')
canvas.pack()      

frame = tk.Frame(root,bg = 'white')
frame.place(relwidth=0.8,relheight=0.7,relx=0.1,rely=0.1)

openFile = tk.Button(root,text="Select File",padx=10,pady=5,fg='white',bg="#263D42" ,command=addApp)

openFile.pack()

runApps = tk.Button(root,text="Run Apps",padx=10,pady=5,fg='white',bg="#263D42", command=runApps)

runApps.pack()
  
# TextBox Creation
inputtxt = tk.Text(root,height=2)  
inputtxt.pack()
# Button Creation
printButton = tk.Button(root,text = "Tag Files",padx=10,pady=5,fg='white',bg="#263D42",command = printInput)
printButton.pack()
# Button Creation
gettagButton = tk.Button(root,text="Get Tagged Files",padx=10,pady=5,fg='white',bg="#263D42", command = gettaggedfiles)
gettagButton.pack()
# Button Creation
getags = tk.Button(root,text="Get tags of the file",padx=10,pady=5,fg='white',bg="#263D42",command = getag_for_file)
getags.pack()
# Button Creation
removetags = tk.Button(root,text="Remove tags",padx=10,pady=5,fg='white',bg="#263D42",command = removetags_for_file)
removetags.pack()
# Button Creation
clear = tk.Button(root, text = "Clear Screen",padx=10,pady=5,fg='white',bg="#263D42",command=reset_apps)
clear.pack()


  

# Label Creation
lbl = tk.Label(frame, text = "")
lbl.pack()

root.mainloop()

with open("tags.txt",'w') as f:
    f.write(str(tags))
    
with open("files.txt",'w') as f:
    f.write(str(files))
        
