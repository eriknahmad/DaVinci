# Project Name: Da Vinci
# File Name: DaVinci.py
# Author: Erik Nahmad
# Date: March 26 2022
# Purpose: Displays Wolfram Alpha / Google results to the GUI.

import tkinter as tk
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import ImageTk, Image
from io import BytesIO
import wolframalpha
import os

class daVinci:
  global driver, font, row, column
  font = ("Helvetica", 10); row = 1; column = 1;
  client = wolframalpha.Client(os.getenv('WOLFRAM'))  # Wolfram Alpha Client
  ChromeOptions = Options()
  ChromeOptions.add_argument("headless");
  ChromeOptions.add_argument('--no-sandbox')
  ChromeOptions.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=ChromeOptions)  # Web Driver to scrape JS


  
  def wolframAlpha(question, frame):
    """Send query to Wolfram Alpha, iterate over each result, and display images to the GUI frame."""
    global wolframResults, row  # Global Variables
    wolframResults = False  # False if query has no results
    daVinci.clearFrame(frame)  # Clear Frame before we start
    query = daVinci.client.query(question).pods  # Request to Wolfram
    
    # for each result display images to GUI and increment the row
    for res in query:  # For each result returned
      wolframResults = True  # True if query has any results
      row = daVinci.wolframToGUI(frame, res)  # Print Wolfram Results to GUI
    daVinci.GoogleResult(frame, question)  # Print Google Result at the end



  def urlToImage(imgURL):
    """Turn URL into PIL.ImageTK.PhotoImage object for TKinter GUI."""
    response = requests.get(imgURL)  # Make Request to URL
    img_data = response.content  # Store the content
    img_bytes = Image.open(BytesIO(img_data))  # Store as bytes
    img = ImageTk.PhotoImage(img_bytes)  # Bytes to img obj for GUI
    return img  # Return PIL.ImageTK.PhotoImage object

    
  
  def imgToGUI(frame, res, img):
    """Place Title and Image Results in a grid."""
    label = tk.Label(frame, text=res, font=font, wraplength=160)  # Init Title
    label.configure(background='white')  # Configure Background Color
    label.grid(sticky="nw", row=row, column=column)  # Pack Title into the GUI
    panel = tk.Label(frame, image=img)  # Init Image Panel
    panel.photo = img  # Display Wolfram Image
    panel.configure(background='white')  # Configure Background Color
    panel.grid(sticky="nw", row=row, column=column+1)  # Pack Image into the GUI


  
  def googleToGUI(frame, res, row, column):
    """Place Google Results in a grid"""
    title = "Google Result: "
    label = tk.Label(frame, text=title, font=font, wraplength=160)  # Init Title
    label.configure(background='white')  # Configure Background Color
    label.grid(sticky="nw", row=row, column=column)  # Pack Title into the GUI
    result = tk.Label(frame, text=res, font=font, wraplength=500)  # Init Google Result
    result.configure(background='white')  # Configure Background Color
    result.grid(sticky="nw", row=row, column=column+1)  # Pack Google Result into the GUI


  
  def clearFrame(frame):
    """Clear frame contents for new results"""
    for element in frame.winfo_children():  # Loop over frame contents
      element.destroy()  # Destroy each element in the frame


  
  def emptySpace(frame):
    """Print new line in the GUI"""
    daVinci.imgToGUI(frame, "", "")

      

  ### Scary Code ###

      
  
  def wolframToGUI(frame, res):
    """Place Wolfram Result in a grid"""
    global row  # Global Variable
    dv = daVinci  # Shorten method calls
    header = f"{res.title}: "  # Store Pod Title as Header

    if type(res.subpod) == list:  # if result object is a list
      if res.subpod[0].title == "":  # if first title is empty
        emptyFirst = True  # Remember state for later
      else:  # If first obj has title then print it as a header
        dv.imgToGUI(frame, header, "")  # Header
        emptyFirst = False  # Rembember state for later
        row += 1  # Next row
      # Titles for subpods
      for subpod in res.subpod:  # for each object in list
        title = f"{subpod.title}: "  # store title of each
        if (emptyFirst):  # if emptyFirst use original title
          title = header  # Original Title / Header
          emptyFirst = False  # No longer empty
        elif subpod.title == "":  # If empty subpod title
          title = ""  # Store empty string
        # Print current subpod title and img
        img = dv.urlToImage(subpod.img.src)
        dv.imgToGUI(frame, title, img)
        row += 1

    else:  # if result type is simply a subpod
      # Print results
      imageURL = res.subpod.img.src
      img = dv.urlToImage(imageURL)
      dv.imgToGUI(frame, header, img)
    row += 1
    dv.emptySpace(frame)
    row += 1
    return row


    
  def GoogleResult(frame, question):
    """Scrape google results and print to GUI."""
    url = "https://www.google.com/search?q=" + question
    driver.get(url)  # Load URL in Selenium to scrape JavaScript
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    title = soup.select_one('.Z0LcW')
    sample = soup.select_one('.hgKElc')
    dv = daVinci

    try:  # remove g-bubble for some questions
      remove = sample.find("g-bubble")
      header = remove.find("span").find("span")
      remove.replaceWith(header)
      sample.replaceWith(remove)
    except:
      pass

    try:  # Print Google Results on GUI
      dv.googleToGUI(frame, title.text, row, column)
      dv.googleToGUI(frame, sample.text, row+1, column)
      if wolframResults == False: print("No Wolfram Results")
    except:
      try:
        dv.googleToGUI(frame, sample.text, row, column)
        if wolframResults == False: print("No Wolfram Results")
      except:
        if wolframResults == False:
          label = tk.Label(frame, text="No Results.", font=font, wraplength=160)
          label.configure(background='white')
          label.grid(sticky="nw", row=row, column=column)
          print("No Results")
        else:
          print("No Google Results.")

