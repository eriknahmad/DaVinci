# Project Name: Da Vinci
# File Name: GUI.py
# Author: Erik Nahmad
# Date: March 26 2022
# Purpose: Initialize GUI elements and control key down events

import tkinter as tk
from DaVinci import daVinci 

class GUI:
  global font, font2, question
  font = ("Helvetica", 10)
  font2 = ("Helvetica", 9)
  question = None


  
  def Start():  # Create window and gui elements
    root = GUI.initializeGUI()  # Initialize Window
    GUI.initGUILabel()  # Label Prompting For User Input
    GUI.initGUIInput()  # User Input Text Box
    GUI.initGUIButton()  # Button to send query
    GUI.initGUIQuestionLabel()  # Display Question
    GUI.initGUICanvas()  # Canvas for scroll bar
    GUI.initGUIScrollbar()  # Scroll bar
    GUI.initGUIFrame()  # Frame for results
    GUI.displayIntroMessage()  # Display Intro Message
    GUI.keyDownEvent()  # Events for scroll bar
    return root
    

  
  def initializeGUI():
    """Initialize TKinter GUI Window"""
    global root  # Global Variable
    root = tk.Tk()  # Initialize TKinter Window
    root.geometry("700x400")  # Set Window Size
    root.configure(background='white')  # Window Background
    root.title('Da Vinci')  # Window Title
    return root  # Return Window Object

  
  
  def initGUILabel():
    """Initialize Label Prompting For User Input"""
    label = tk.Label(text="Ask a question: ", font=font)  # Init Label
    label.configure(background='white')  # Configure Background Color
    label.pack(anchor="nw")  # Pack Label into the GUI anchored to the Top Left

  
  
  def initGUIInput():
    """Initialize User Input Textbox"""
    global userInput  # Global Variable
    userInput = tk.Entry(width=30)  # Init User Input Textbox
    userInput.focus_set()  # Start With User Input Widget Selected
    userInput.pack(side="top", anchor="nw")  # Pack into the GUI to the Top Left

  
  
  def initGUIButton():
    """Initialize Button To Send Query"""
    t = "Enter"; w = 28; c = GUI.sendQuery  # Parameters: Text, Width, Command
    button = tk.Button(text=t, width=w, command=c)  # Init Button With Command
    button.pack(side="top", anchor="nw", pady=8)  # Pack into the GUI to the Top Left


  
  def initGUIQuestionLabel():
    """Initialize Label That Displays The Question"""
    global questionLabel  # Global Variable
    questionLabel = tk.Label(text=question, font=font)  # Init QL with User Input
    questionLabel.configure(background='white')  # Configure Background Color
    questionLabel.pack(anchor="nw", pady=6)  # Pack into the GUI to the Top Left


  
  def initGUICanvas():
    """Initialize Canvas for Scrollbar"""
    global canvas  # Global Variable
    canvas = tk.Canvas(root)  # Init Canvas attached to Window
    canvas.configure(bg="white")  # Configure Background Color


  
  def initGUIScrollbar():
    """Initialize Scrollbar"""
    global scroll_y  # Global Variable
    o = "vertical"; c = canvas.yview  # Parameters: Orientation, Command
    scroll_y = tk.Scrollbar(root, orient=o, command=c)  # Init Scrollbar

  

  def initGUIFrame():
    """Initialize Frame"""
    global frame  # Global Variable
    frame = tk.Frame(canvas)  # Init Frame
    frame.configure(background="white")  # Configure Background Color
    canvas.create_window(0, 0, anchor='nw', window=frame)  # Put Frame in Canvas
    GUI.UpdateCanvas()  # Update Canvas before configuring the scrollregion
    canvas.pack(fill='both', expand=True, side='left')  # Pack Canvas into the GUI
    scroll_y.pack(fill='y', side='right')  # Pack Scrollbar into the GUI


    
  def sendQuery():
    """Update Question Label And Send Query To Wolfram"""
    global question  # Global Variable
    question = userInput.get()  # Store User Input
    questionLabel.configure(text=question)  # Display Question
    commands = ['test', 'bob']  # Work On Commands Later
    if question == "": print("Invalid Question.")  # If Empty String
    elif question in commands: pass  # Setup Commands Here
    else:  # If User Input is a valid query - not empty or a command
      daVinci.wolframAlpha(question, frame)  # Display Results
      GUI.UpdateCanvas()  # Update Canvas Height for Scrollbar

    

  def keyDownEvent():
    """Key Down Events for Scrollbar"""
    root.bind("<Return>", GUI.keyup)  # if enter key is pressed then send query
    root.bind("<Up>", lambda event: canvas.yview_scroll(-1, "units"))  # Move Scrollbar Up
    root.bind("<Down>", lambda event: canvas.yview_scroll(1, "units"))  # Move Scrollbar Down


    
  def keyup(event):  # Detect Enter Key Press
    GUI.sendQuery()  # Send Query to Wolfram Alpha and Google

    
   
  def UpdateCanvas():
    """Update Canvas Elements For Scrollbar"""
    canvas.update_idletasks()  # Update Tasks
    canvas.yview_moveto(0)  # Reset canvas / scrollbar position
    canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)  # Set scrollbar to canvas height


  
  def displayIntroMessage():
    """Display Intro Message"""
    title = "Welcome to Da Vinci."
    summary = "An educational bot using the most powerful knowledge engines in the world."
    titleLabel = tk.Label(frame, text=title, font=font, wraplength=400)
    titleLabel.configure(background='white')
    titleLabel.grid(sticky="nw", row=0, column=0)
    summaryLabel = tk.Label(frame, text=summary, font=font2, wraplength=550)
    summaryLabel.configure(background='white')
    summaryLabel.grid(sticky="nw", row=1, column=0)
