
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException
import pandas as pd
import time
from datetime import datetime,date,timedelta
import rtsfuncs

email = 'YOUR_EMAIL' #RTS email
password = 'YOUR_PASSWORD' #RTS password 
ls_csv_name = ['rtsday1.csv'] #csv filenames eg: ['rtsday1.csv', 'rtsday2.csv',...]
save_status = True #just use true 
num_micros = 1 #number of weeks
driver = 'chromedriver' #browser driver to use


rtsfuncs.complete_macro(email, password, ls_csv_name, save_status, num_micros, driver)