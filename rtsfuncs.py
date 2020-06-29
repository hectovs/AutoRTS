from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException
import pandas as pd
import time
from datetime import datetime,date,timedelta

def login(email, password, driver):
    chrome_browser = webdriver.Chrome(f'./{driver}')
    chrome_browser.maximize_window()
    chrome_browser.get('https://www.reactivetrainingsystems.com/Authentication/LoginPage') 
    
    user_email = chrome_browser.find_element_by_id("Username")
    user_email.clear()
    user_email.send_keys(f'{email}')
    
    user_pass = chrome_browser.find_element_by_id("Password")
    user_pass.clear()
    user_pass.send_keys(f'{password}')
    
    submit_button = chrome_browser.find_element_by_css_selector('#LoginForm2 > div.pull-right > button.btn.btn-default')
    submit_button.click()
    return chrome_browser


def create_workout(w_date, ls_exercises, chrome_browser):
    chrome_browser.get(f'https://www.reactivetrainingsystems.com/Traininglog/AddWorkout?StartDate={w_date}')
    
    for ex_name in ls_exercises:
        exercise = chrome_browser.find_element_by_xpath(f"//*[text()='{ex_name}']")
        exercise.click()
        time.sleep(0.25)

    cont = chrome_browser.find_element_by_id('TlContinue')
    cont.click() #click to create workout


def fill_workout(exer_num_ls, num_sets, weight_ls, rep_ls, rpe_ls, chrome_browser):
    
    set_num = chrome_browser.find_element_by_css_selector('#IExerciseList > li:nth-child(1) > div.IRow > div.IInlineContainer > span > input')
    set_num.send_keys(num_sets) #input number of sets

    expand = chrome_browser.find_element_by_id("AutoSaveHeader")
    expand.click() #click outside are to reveal forms
    time.sleep(1)

    fill_weights = chrome_browser.find_element_by_css_selector('#IExerciseList > li:nth-child(1) > div.IExpandable > div:nth-child(2) > div.Actual > span:nth-child(1) > input')
    fill_weights.send_keys(weight_ls)

    fill_reps = chrome_browser.find_element_by_css_selector('#IExerciseList > li:nth-child(1) > div.IExpandable > div:nth-child(2) > div.Actual > span:nth-child(4) > input')
    fill_reps.send_keys(rep_ls)

    fill_rpe = chrome_browser.find_element_by_css_selector('#IExerciseList > li:nth-child(1) > div.IExpandable > div:nth-child(2) > div.Actual > span:nth-child(6) > input')
    fill_rpe.send_keys(rpe_ls)


def open_mods(id, chrome_browser):
    #open modifier window
    open_mod = chrome_browser.find_element_by_css_selector(f'#IExerciseList > li:nth-child({id}) > div.IRow > div.ActionExp > div:nth-child(4) > a > img')    
    open_mod.click()
    time.sleep(0.5)


def add_mods(mod_type, mod_name,chrome_browser):

    #kit 
    mod_type_ele = chrome_browser.find_element_by_css_selector('#ModTabs > div:nth-child(4)')
    mod_type_ele.click()
    
    time.sleep(1)
    mod_name_ele = chrome_browser.find_element_by_xpath(f"//*[text()='{mod_name}']")
    mod_name_ele.click()

def add_mods2(mod_name_ls, chrome_browser):

    for i in range(7):
        n=i+1
        n=str(n)
        mod_type_ele = chrome_browser.find_element_by_css_selector(f'#ModTabs > div:nth-child({n})')
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
                print('that modifier does not exist')
                break
    
    save_ele = chrome_browser.find_element_by_css_selector('#ApplyExBut')
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
    
def fill_workout2(exer_num_ls, num_sets_ls, ls_weights_ls, ls_reps_ls, ls_rpe_ls, ls_mods_ls, ls_exercises, chrome_browser):
    #two for loops one for exercises one for sets 
    for num in range(len(ls_exercises)):
        
        m = num+1

        open_mods(m, chrome_browser)
        add_mods2(ls_mods_ls[num], chrome_browser)
        
        set_num = chrome_browser.find_element_by_css_selector(f'#IExerciseList > li:nth-child({m}) > div.IRow > div.IInlineContainer > span > input')
        set_num.send_keys(num_sets_ls[num])

        expand = chrome_browser.find_element_by_id("AutoSaveHeader")
        expand.click()
        time.sleep(0.75)

        for i in range(len(ls_weights_ls[num])):
            n=i+2
            fill_weights = chrome_browser.find_element_by_css_selector(f'#IExerciseList > li:nth-child({m}) > div.IExpandable > div:nth-child({n}) > div.Actual > span:nth-child(1) > input')
            weights = ls_weights_ls[num][i]
            fill_weights.send_keys(weights)

            fill_reps = chrome_browser.find_element_by_css_selector(f'#IExerciseList > li:nth-child({m}) > div.IExpandable > div:nth-child({n}) > div.Actual > span:nth-child(4) > input')
            reps = ls_reps_ls[num][i]
            fill_reps.send_keys(reps)

            fill_rpe = chrome_browser.find_element_by_css_selector(f'#IExerciseList > li:nth-child({m}) > div.IExpandable > div:nth-child({n}) > div.Actual > span:nth-child(6) > input')
            rpe = ls_reps_ls[num][i]
            fill_rpe.send_keys(rpe)

def save_workout(option, chrome_browser):
    save = chrome_browser.find_element_by_css_selector('#SaveWorkout')
    if option:
        save.click()
        print('The workout was saved')
    else:
        print('The workout was not saved')
        chrome_browser.quit()
        chrome_browser.quit()

   

def complete_workout(email,password,csv_name,save_status, driver):

    chrome_browser = login(email, password, driver)

    num_sets_ls, exer_num_ls, w_date, ls_exercises, ls_mods_ls, ls_weights_ls, ls_reps_ls, ls_rpe_ls = extract_vars(f'{csv_name}')
            
    create_workout(w_date,ls_exercises, chrome_browser)
    time.sleep(1)

    fill_workout2(exer_num_ls, num_sets_ls, ls_weights_ls, ls_reps_ls, ls_rpe_ls, ls_mods_ls, ls_exercises, chrome_browser)
    save_workout(save_status,chrome_browser)


def complete_macro(email,password,ls_csv_name,save_status, num_micros, driver):

    ls_w_date = []  
    chrome_browser = login(email, password,driver)

    for csv_name in ls_csv_name:
        
        num_sets_ls, exer_num_ls, w_date, ls_exercises, ls_mods_ls, ls_weights_ls, ls_reps_ls, ls_rpe_ls = extract_vars(f"{csv_name}")

        for num in range(num_micros):
            
            ls_w_date.append(w_date)

            dyn_date = datetime.strptime(w_date, "%m/%d/%Y")
            next_date = dyn_date + timedelta(days=7)

            w_date = next_date.strftime("%m/%d/%Y")

        

        for date in ls_w_date: 
            print(date)        
            create_workout(date,ls_exercises,chrome_browser)
            time.sleep(1)

            fill_workout2(exer_num_ls, num_sets_ls, ls_weights_ls, ls_reps_ls, ls_rpe_ls, ls_mods_ls, ls_exercises, chrome_browser)
            save_workout(save_status,chrome_browser)
            time.sleep(2)

        time.sleep(30)



