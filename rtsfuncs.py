from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime,date,timedelta

def initialise_se(driver):
    global chrome_browser 
    chrome_browser = webdriver.Chrome(f'./{driver}')
    chrome_browser.maximize_window()

def login(email, password):

    chrome_browser.get('https://www.reactivetrainingsystems.com/Authentication/LoginPage') 
    
    user_email = WebDriverWait(chrome_browser,10, poll_frequency=0.25).until(EC.presence_of_element_located((By.ID,("Username"))))
    user_email.clear()
    user_email.send_keys(f'{email}')
    
    user_pass = WebDriverWait(chrome_browser,10, poll_frequency=0.25).until(EC.presence_of_element_located((By.ID,("Password"))))
    user_pass.clear()
    user_pass.send_keys(f'{password}')
    
    submit_button = WebDriverWait(chrome_browser,10, poll_frequency=0.25).until(EC.presence_of_element_located((By.CSS_SELECTOR,('#LoginForm2 > div.pull-right > button.btn.btn-default'))))   
    submit_button.click()
    return chrome_browser


def create_workout(w_date, ls_exercises):
    chrome_browser.get(f'https://www.reactivetrainingsystems.com/Traininglog/AddWorkout?StartDate={w_date}')
    
    for ex_name in ls_exercises:
        exercise = WebDriverWait(chrome_browser,10, poll_frequency=0.50).until(EC.element_to_be_clickable((By.XPATH,(f"//*[text()='{ex_name}']"))))
        exercise.click()
        time.sleep(0.25)
        
    time.sleep(0.25)
    cont = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.element_to_be_clickable((By.ID,('TlContinue'))))
    cont.click() #click to create workout


def fill_workout(exer_num_ls, num_sets, weight_ls, rep_ls, rpe_ls):
    
    set_num = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.CSS_SELECTOR,('#IExerciseList > li:nth-child(1) > div.IRow > div.IInlineContainer > span > input'))))
    set_num.send_keys(num_sets) #input number of sets

    expand = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.ID,("AutoSaveHeader"))))
    expand.click() #click outside are to reveal forms
    time.sleep(1)

    fill_weights = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ('#IExerciseList > li:nth-child(1) > div.IExpandable > div:nth-child(2) > div.Actual > span:nth-child(1) > input'))))
    fill_weights.send_keys(weight_ls)

    fill_reps = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.CSS_SELECTOR,('#IExerciseList > li:nth-child(1) > div.IExpandable > div:nth-child(2) > div.Actual > span:nth-child(4) > input'))))
    fill_reps.send_keys(rep_ls)

    fill_rpe =WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.CSS_SELECTOR,('#IExerciseList > li:nth-child(1) > div.IExpandable > div:nth-child(2) > div.Actual > span:nth-child(6) > input'))))
    fill_rpe.send_keys(rpe_ls)


def open_mods(id):
    #open modifier window
    open_mod = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.CSS_SELECTOR, (f'#IExerciseList > li:nth-child({id}) > div.IRow > div.ActionExp > div:nth-child(4) > a > img'))))    
    open_mod.click()
    


def add_mods(mod_type, mod_name):

    #kit 
    mod_type_ele = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ('#ModTabs > div:nth-child(4)'))))
    mod_type_ele.click()
    
    time.sleep(1)
    mod_name_ele = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.XPATH,(f"//*[text()='{mod_name}']"))))
    mod_name_ele.click()

def add_mods2(mod_name_ls):

    for i in range(7):
        n=i+1
        n=str(n)
        mod_type_ele = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.CSS_SELECTOR,(f'#ModTabs > div:nth-child({n})'))))
        mod_type_ele.click()
        time.sleep(0.15)
        for mod_name in mod_name_ls:
            try: 
                mod_name_ele = chrome_browser.find_element_by_xpath(f"//*[text()='{mod_name}']")
                mod_name_ele.click()
                time.sleep(0.15)
            except ElementNotInteractableException:
                time.sleep(0.15)
                continue
            except NoSuchElementException:
                print(f'that modifier {mod_name} does not exist')
                break
    
    save_ele = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.CSS_SELECTOR,('#ApplyExBut'))))
    save_ele.click()


def extract_vars(csv_name):
    day = pd.read_csv(f'{csv_name}')
    exer_num_ls = []
    ls_exercises = []
    num_sets_ls = []
    ls_mods_ls = []
    ls_weights_ls = []
    ls_reps_ls = []
    ls_rpe_ls = []

    for exer_num,group in day.groupby(['exercise number']):
        
        exercise = group['exercise'].iloc[0]
        w_date = group['workout date'].iloc[0]
        mods = group['modifiers'].iloc[0]
        exer_num_ls.append(exer_num)
        mods_ls = str(mods).split(',')

        weight_ls = []
        reps_ls = []
        rpe_ls = []

        for index, row in group.iterrows():

            weight_ls.append(row['weight'])
            reps_ls.append(row['reps'])
            rpe_ls.append(row['rpe'])
            
        ls_mods_ls.append(mods_ls)
        ls_exercises.append(str(exercise))
        ls_weights_ls.append(weight_ls)
        ls_reps_ls.append(reps_ls)
        ls_rpe_ls.append(rpe_ls)

        
        num_sets = len(group)
        num_sets_ls.append(num_sets)
        
    # print(num_sets_ls, exer_num_ls, w_date, ls_exercises, ls_mods_ls, ls_weights_ls, ls_reps_ls, ls_rpe_ls)
    return num_sets_ls, exer_num_ls, w_date, ls_exercises, ls_mods_ls, ls_weights_ls, ls_reps_ls, ls_rpe_ls 
    
def fill_workout2(exer_num_ls, num_sets_ls, ls_weights_ls, ls_reps_ls, ls_rpe_ls, ls_mods_ls, ls_exercises):
    #two for loops one for exercises one for sets 
    for num in range(len(ls_exercises)):
        
        m = num+1

        open_mods(m)
        add_mods2(ls_mods_ls[num])
        
        set_num = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.CSS_SELECTOR,(f'#IExerciseList > li:nth-child({m}) > div.IRow > div.IInlineContainer > span > input'))))
        set_num.send_keys(num_sets_ls[num])

        expand = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.ID,("AutoSaveHeader"))))
        expand.click()
        

        for i in range(len(ls_weights_ls[num])):
            n=i+2
            fill_weights = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.CSS_SELECTOR,(f'#IExerciseList > li:nth-child({m}) > div.IExpandable > div:nth-child({n}) > div.Actual > span:nth-child(1) > input'))))
            weights = ls_weights_ls[num][i]
            fill_weights.send_keys(weights)

            fill_reps = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.CSS_SELECTOR,(f'#IExerciseList > li:nth-child({m}) > div.IExpandable > div:nth-child({n}) > div.Actual > span:nth-child(4) > input'))))
            reps = ls_reps_ls[num][i]
            fill_reps.send_keys(reps)

            fill_rpe = WebDriverWait(chrome_browser,10, poll_frequency=0.20).until(EC.presence_of_element_located((By.CSS_SELECTOR,(f'#IExerciseList > li:nth-child({m}) > div.IExpandable > div:nth-child({n}) > div.Actual > span:nth-child(6) > input'))))
            rpe = ls_reps_ls[num][i]
            fill_rpe.send_keys(rpe)

def save_workout(option):
    save = WebDriverWait(chrome_browser,10, poll_frequency=0.2).until(EC.presence_of_element_located((By.CSS_SELECTOR,('#SaveWorkout'))))
    if option:
        save.click()
        print('The workout was saved')
    else:
        print('The workout was not saved')
        chrome_browser.quit()
        chrome_browser.quit()

   

def complete_workout(email,password,csv_name,save_status):

    login(email, password)

    num_sets_ls, exer_num_ls, w_date, ls_exercises, ls_mods_ls, ls_weights_ls, ls_reps_ls, ls_rpe_ls = extract_vars(f'{csv_name}')
            
    create_workout(w_date,ls_exercises)
    time.sleep(1)

    fill_workout2(exer_num_ls, num_sets_ls, ls_weights_ls, ls_reps_ls, ls_rpe_ls, ls_mods_ls, ls_exercises)
    save_workout(save_status)


def complete_macro(email,password,ls_csv_name,save_status, num_micros, driver):

    ls_w_date = []  
    initialise_se(driver)
    login(email, password)

    for csv_name in ls_csv_name:
        
        num_sets_ls, exer_num_ls, w_date, ls_exercises, ls_mods_ls, ls_weights_ls, ls_reps_ls, ls_rpe_ls = extract_vars(f"{csv_name}")

        for num in range(num_micros):
            
            ls_w_date.append(w_date)

            dyn_date = datetime.strptime(w_date, "%m/%d/%Y")
            next_date = dyn_date + timedelta(days=7)

            w_date = next_date.strftime("%m/%d/%Y")

        

        for date in ls_w_date: 
            print(date)        
            create_workout(date,ls_exercises)
            time.sleep(1)

            fill_workout2(exer_num_ls, num_sets_ls, ls_weights_ls, ls_reps_ls, ls_rpe_ls, ls_mods_ls, ls_exercises)
            save_workout(save_status)
            time.sleep(2)

        time.sleep(30)


