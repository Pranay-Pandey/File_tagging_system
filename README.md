# File Tagging System

This development is a part of <b><a href='https://unstop.com/hackathon/tally-codebrewers-tally-solutions-343510'>Tally CodeBrewers</a> <a href='https://tallysolutions.com/'>Tally Solutions</a></b>.

<h3>File Tagging</h3>
A software that will help users organize their Files on disk using Tags.<br>
• A tag is an arbitrary value that can be associated with a file. (Like names of people, 
places, events, etc.)<br>
• Users will be able to tag their files and locate them using tags.<br>
• A file can be associated with multiple tags, and a tag can be associated with multiple 
files.<br>
• Something like how an email-client help organize emails using 
labels.<br>

The code is written in python programming language and is tested to run on windows and ubuntu systems.

The problem statement of the competetion can be assesed from [here](https://github.com/Pranay-Pandey/File_tagging_system/files/9130326/ProblemStatement_WizardofSystemProgramming.pdf)

The software is integrated with the tkinter GUI and has the buttons:
<br><b>Select File</b>: Select all the files to tag
<br><b>Run Apps</b>: Run all the files selected(user has to enter the index of these files through the text box seperated by spaces)
<br><b>Tag Files</b>: First select all files wished to be tagged using Select file and then type the name of the tags wished to be associated wth those files in the text box seperated by spaces
<br><b>Get tagged files</b>: Write tags in the text box seperated by spaces (for AND operation) separeted by /(for OR operation) prefixed by ~(for NOT operation) and then click this button to get all files with the given tags. Clicking this button with empty text box returns all the tags present in the file system
<br><b>Get tags of a file</b>: Show all the tags of a file (file index to be typed through the text box)
<br><b>Remove tags</b>: After getting all tags of a file, type the tag names you wish to unassociate with the file then click on this button
<br><b>Clear Screen</b>: Clear the screen 


![image](https://user-images.githubusercontent.com/79053599/179468777-f3aaa28f-d3f2-4f07-a477-4f719b6d4029.png)


The working of the system is basaed on two dictionary: tags and files which are saved locally as text file in the same directory as the python file.
