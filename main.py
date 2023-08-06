from tkinter import *
from tkinter import messagebox
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException

import webbrowser
import os
import time
import getpass
import random
import string
import re

root = Tk()  # create parent window
root.title("Upwork Account Creator")
root.minsize(200, 200)  # width, height
root.geometry("215x230+50+50")

process_flag = False
totoal_count = 0
current_count = 0

def checkavailable():
    global process_flag
    global totoal_count
    global current_count
    if process_flag == True:
        messagebox.showinfo("Alert", "It's already processing...")
        
    if email_input.get() == '':
        messagebox.showerror('Alert', 'Enter email')
        return
    
    if skill_input.get() == '':
        messagebox.showerror('Alert', 'Enter skills separating by comma')
        return
    
    acc_counts = accounts_count.get()
    print("Volume Increase +1")

    with open('upwork.csv') as f:
        reader = csv.DictReader(f)
        csv_data = list(reader)
        csv_data_count = len(csv_data)
        acc_counts = int(acc_counts)
        totoal_count = acc_counts
        current_count = 0
        
        process_flag = True
        stat_label_result.config(text="Processing...", fg="blue")
        while current_count < acc_counts:
            stat_label.config(text=f"{current_count}/{totoal_count}")
            try:
                index = current_count % csv_data_count
                csv_data[index]['Email'] = email_input.get()
                csv_data[index]['Skills'] = skill_input.get()
                create_account(csv_data[index], profile_input.get())
            except Exception as ex:
                print(ex, current_count + 1)
                stat_label_result.config(text="Failed!", fg="red")
            current_count += 1
    process_flag = False

def create_account(person_info, profile):
    username = getpass.getuser()
    if username == "root":
        username = "Administrator"

    # Connect to a currently opened chrome driver with a remote debugging port
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9124")
    
    driver = webdriver.Chrome(options=chrome_options)
    actions = ActionChains(driver)
    print(driver)
    
    driver.get("https://www.upwork.com/nx/signup/")
    driver.maximize_window()

    try:
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="main"]/div/div/div/div/div/div/div[1]/fieldset/div/div[2]/div/div[1]/label')))
        freelancer_choice_btn = driver.find_element(By.XPATH,
                                   '//*[@id="main"]/div/div/div/div/div/div/div[1]/fieldset/div/div[2]/div/div[1]/label')    
    except:
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="main"]/div/div/div/div/div/div/div[1]/fieldset/div/div[2]/div/div[1]/label')))
        freelancer_choice_btn = driver.find_element(By.XPATH,
                                   '//*[@id="main"]/div/div/div/div/div/div/div[1]/fieldset/div/div[2]/div/div[1]/label')    
    # Select freelancer and click next
    freelancer_choice_btn.send_keys(Keys.ENTER)
    driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/div/div/div/div[2]/button').click()
    
    ########################################################## Start registration ##########################################################
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
        cookie_accept_btn = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        cookie_accept_btn.click()
    except:
        pass
        print('Passed')

    driver.find_element(By.XPATH, '//*[@id="first-name-input"]').send_keys(person_info['First_Name'])
    driver.find_element(By.XPATH, '//*[@id="last-name-input"]').send_keys(person_info["Last_Name"])
    driver.find_element(By.XPATH, '//*[@id="redesigned-input-email"]').send_keys(person_info['Email'])
    driver.find_element(By.XPATH, '//*[@id="password-input"]').send_keys(person_info['Password'])
    driver.find_element(By.XPATH, '//*[@id="signupForm-redesigned"]//div[@data-test="dropdown-toggle"]').click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'up-dropdown-menu-container')))
    driver.find_element(By.XPATH, '//input[@autocomplete="country-name"]').click()
    driver.find_element(By.XPATH, '//input[@autocomplete="country-name"]').send_keys(person_info['Country'])
    driver.find_element(By.XPATH, '//input[@autocomplete="country-name"]').send_keys(Keys.ARROW_DOWN, Keys.ENTER)
    driver.find_element(By.XPATH, '//*[@id="signupForm-redesigned"]/fieldset/div[2]/label/span').click()

    driver.find_element(By.XPATH, '//*[@id="button-submit-form"]').click()
    print('clicked')
    ########################################################### End registration ###########################################################

    try:
        WebDriverWait(driver, 300).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]//button/span[contains(text(), "Get started")]')))
        driver.find_element(By.XPATH, '//*[@id="main"]//button/span[contains(text(), "Get started")]').click()
    except:
        WebDriverWait(driver, 300).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]//button/span[contains(text(), "Get started")]')))
        driver.find_element(By.XPATH, '//*[@id="main"]//button/span[contains(text(), "Get started")]').click()
    print("after get started")
        
    try:
        WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//h2[contains(text(), "have you freelanced before")]')))
    except:
        WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//h2[contains(text(), "have you freelanced before")]')))
    
    try:
        driver.find_element(
        By.XPATH,
        '//h4[contains(text(), "I am an expert")]').click()
    except:
        driver.find_element(
        By.XPATH,
        '//h4[contains(text(), "I am an expert")]').click()
    try:
        next_button = driver.find_element(By.XPATH, '//button[contains(text(), "Next")]')
        next_button.click()
    except:
        next_button = driver.find_element(By.XPATH, '//button[contains(text(), "Next")]')
        next_button.click()
    print('button')
    try:
        WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//h4[contains(text(), "To earn my main income")]')))
        driver.find_element(By.XPATH, '//h4[contains(text(), "To earn my main income")]').click()
    except:
        WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//h4[contains(text(), "To earn my main income")]')))
        driver.find_element(By.XPATH, '//h4[contains(text(), "To earn my main income")]').click()

    print('To earn my main income')
    try:
        driver.find_element(By.XPATH, '//button[contains(text(), "Next")]').click()
    except:
        driver.find_element(By.XPATH, '//button[contains(text(), "Next")]').click()
    print("Next click()")
    try:
        WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//h4[contains(text(), "opportunities myself")]')))
        driver.find_element(By.XPATH, '//h4[contains(text(), "opportunities myself")]').click()
    except:
        WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//h4[contains(text(), "opportunities myself")]')))
        driver.find_element(By.XPATH, '//h4[contains(text(), "opportunities myself")]').click()
    print("wait complete")

    # # time.sleep(5)
    print('finished 0')
    try:
        driver.find_element(By.XPATH, '//h4[contains(text(), "I’d like to package up my work for clients to buy")]').click()
    except:
        driver.find_element(By.XPATH, '//h4[contains(text(), "I’d like to package up my work for clients to buy")]').click()
    # # time.sleep(5)
    print('finished 1')
    try:
        driver.find_element(By.XPATH, '//strong').click()
    except:
        driver.find_element(By.XPATH, '//strong').click()
    # # time.sleep(5)
    print('finished 2')
    try:
        driver.find_element(By.XPATH, '//button[contains(text(), "create")]').click()
    except:
        driver.find_element(By.XPATH, '//button[contains(text(), "create")]').click()
    print('finished 3')
    ############################################## Step 1/10 How would you like to tell us about yourself? ##############################################
    # Click 'Upload your resume' button
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]/button[2]')))
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]/button[2]').click()
    except:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]/button[2]')))
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]/button[2]').click()
    
    # Upload resume
    resume_path = os.path.dirname(os.path.abspath(__file__)) + rf"/resumes/{person_info['Resume']}"
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/div/p/span/input')))
        driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/div/p/span/input').send_keys(resume_path)
    except:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/div/p/span/input')))
        driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/div/p/span/input').send_keys(resume_path)

    time.sleep(3)
    # Click 'continue'
    driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div[3]/div/button').click()
    
    ############################################## Step 1/10 How would you like to tell us about yourself? ##############################################
    ######################################### Step 2/10 Got it. Now, add a title to tell the world what you do.#########################################
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button')))
        driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()
        
    except:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button')))
        driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()
    time.sleep(0.5)
    # Next, add your experience
        
    ######################################### Step 2/10 Got it. Now, add a title to tell the world what you do.#########################################
    ######################################### Step 3/10 Here’s what you’ve told us about your experience — any more to add? #########################################
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[3]/div/div[2]/div[1]/div/div[2]/ul/li[1]/div[1]')))
        driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()
        
    except:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[3]/div/div[2]/div[1]/div/div[2]/ul/li[1]/div[1]')))
        driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()
    time.sleep(0.5)
    ######################################### Step 3/10 Here’s what you’ve told us about your experience — any more to add? #########################################

    ######################################### Step 4/10 And here’s what we picked up on your education – is it right? #########################################
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[4]/div/div[2]/div[1]/div/div[2]/ul/li[1]/div[1]')))
        driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()
        
    except:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[4]/div/div[2]/div[1]/div/div[2]/ul/li[1]/div[1]')))
        driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()
    time.sleep(0.5)
    ######################################### Step 4/10 And here’s what we picked up on your education – is it right? #########################################

    ######################################### Start Step 5/10 Looking good. Next, tell us which languages you speak. #########################################
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div/div/div/span')))
        driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()
        
    except:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div/div/div/span')))
        driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()
    time.sleep(0.5)
    ######################################### End Step 5/10 Looking good. Next, tell us which languages you speak. #########################################

    ######################################### Start Step 6/10 Nearly there! What work are you here to do? #########################################
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div//input[@placeholder="Enter skills here"]')))
    skills = person_info['Skills'].split(',')
    for skill in skills:
        # time.sleep(1)
        driver.find_element(By.XPATH,
                            '/html/body/div//input[@placeholder="Enter skills here"]').click()
        # time.sleep(1)
        driver.find_element(By.XPATH,
                            '/html/body/div//input[@placeholder="Enter skills here"]').send_keys(skill.strip())
        time.sleep(1.5)
        actions.send_keys(Keys.ARROW_DOWN).perform()
        actions.send_keys(Keys.ENTER).perform()
    
    driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()
    time.sleep(0.5)
    ######################################### End Step 6/10 Looking good. Next, tell us which languages you speak. #########################################

    ######################################### Start Step 7/10 Great! Now write a bio to tell the world about yourself. #########################################
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[7]/div/div/div[1]/div[2]/div/div/div/textarea')))

    if profile != '':
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div//textarea[@data-test="overview"]')))
        driver.find_element(By.XPATH, '/html/body/div//textarea[@data-test="overview"]').click()
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
        driver.find_element(By.XPATH, '/html/body/div//textarea[@data-test="overview"]').send_keys(profile)

    driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()    
    time.sleep(0.5)
    ######################################### End Step 7/10 Great! Now write a bio to tell the world about yourself. #########################################

    ######################################### Start Step 8/10 What are the main services you offer? #########################################
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[8]/div/div[2]/div/div[1]/div/div/div/div/span')))
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[8]/div/div[2]/div/div[2]/button[2]').click()
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()
    except:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[8]/div/div[2]/div/div[1]/div/div/div/div/span')))
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[8]/div/div[2]/div/div[2]/button[2]').click()
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()
    time.sleep(0.5)
    ######################################### End Step 8/10 What are the main services you offer? #########################################
    
    ######################################### Start Step 9/10 Now, let’s set your hourly rate. #########################################
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[9]/div/div[2]/div[1]/div/div[2]/div/div/div/div/input')))
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[9]/div/div[2]/div[1]/div/div[2]/div/div/div/div/input').click()
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[9]/div/div[2]/div[1]/div/div[2]/div/div/div/div/input').send_keys(35)
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()
    except:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[9]/div/div[2]/div[1]/div/div[2]/div/div/div/div/input')))
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[9]/div/div[2]/div[1]/div/div[2]/div/div/div/div/input').click()
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[9]/div/div[2]/div[1]/div/div[2]/div/div/div/div/input').send_keys(30)
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()
    time.sleep(0.5)
    ######################################### End Step 9/10 Now, let’s set your hourly rate. #########################################

    ######################################### End Step 10/10 A few last details, then you can check and publish your profile. #########################################
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[10]/div/div[2]/div/div[1]/div/div/div/button/img')))
    driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div/div[10]/div/div[2]/div/div[1]/div/div/div/button/img').click()
    
    upload_img = os.path.dirname(os.path.abspath(__file__)) + rf"/images/{person_info['Image_Name']}"
    print(upload_img)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/input')))
    driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/input').send_keys(upload_img)
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div[2]/div/button[2]').click()
    
    time.sleep(1)
    # // Reant

    street = fr"{person_info['Street']}"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div//input[@aria-labelledby="street-label"]')))
    driver.find_element(By.XPATH, '/html/body/div//input[@aria-labelledby="street-label"]').click()
    driver.find_element(By.XPATH, '/html/body/div//input[@aria-labelledby="street-label"]').send_keys(street)

    actions.send_keys(Keys.PAGE_DOWN).perform()
    # time.sleep(1.5)
    city = fr"{person_info['City']}"
    driver.find_element(By.XPATH, '/html/body/div//input[@aria-labelledby="city-label"]').click()
    driver.find_element(By.XPATH, '/html/body/div//input[@aria-labelledby="city-label"]').send_keys(city)
    time.sleep(1.5)
    actions.send_keys(Keys.ARROW_DOWN, Keys.ENTER).perform()

    phone = person_info['Phone']
    # time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div//input[@placeholder="Enter number"]').click()
    driver.find_element(By.XPATH, '/html/body/div//input[@placeholder="Enter number"]').send_keys(phone)

    driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/span/button').click()

    # Submit
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/main/div/div/div/div[1]/div[2]/div/div/div[1]/div[2]/button')))
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/main/div/div/div/div[1]/div[2]/div/div/div[1]/div[2]/button').click()
    ######################################### End Step 10/10 A few last details, then you can check and publish your profile. #########################################

def modify_profile():
    pass
    
if __name__ == '__main__':

    text = Label(root, text="How many accounts would you create?")
    text.grid(row=0)
    accounts_count = Entry(root, bd=5, width=30)
    accounts_count.insert(END, 1)
    accounts_count.grid(row=1)

    text = Label(root, text="Email")
    text.grid(row=2)
    email_input = Entry(root, bd=5, width=30)
    email_input.grid(row=3)

    stat_label = Label(root)
    stat_label.grid(row=10, column=0)

    stat_label_result = Label(root)
    stat_label_result.grid(row=10, column=1)

    # Modify Profile
    text = Label(root, text="Profile")
    text.grid(row=4)
    profile_input = Entry(root, bd=5, width=30)
    profile_input.grid(row=5)

    text = Label(root, text="Skills")
    text.grid(row=6)
    skill_input = Entry(root, bd=5, width=30)
    skill_input.grid(row=7)

    modify_btn = Button(root, text="Create", command=checkavailable)
    modify_btn.grid(row=8)
    root.mainloop()

