# -*-coding: utf-8 -*-
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from tkinter import messagebox, Entry, Label, Button, Tk, N, S, W, E
import os
import pickle
import sys

content = 0
count = 0
interval = 0
check = {'content': 0, 'count': 0, 'interval': 0}
check2 = {'email': 0, 'pw': 0}
info = dict()
z = 0

window = Tk()
progress_label = Label(window, text="Waiting for input...")
progress_label.grid(row=5, column=1)


def email_input(event):
    """get email when user registers"""
    global info, check2
    email = str(Entry.get(email_entry))
    email_check["text"] = "OK"
    email_check["fg"] = "green"
    check2['email'] = 1
    info['email'] = email
    return email


def pw_input(event):
    """get password when user registers"""
    global info, check2
    pw = str(Entry.get(pw_entry))
    pw_check["text"] = "OK"
    pw_check["fg"] = "green"
    check2['pw'] = 1
    info['pw'] = pw
    return pw


def register():
    """makes cache file for login"""
    global info, check2
    for x, y in check2.items():
        if y == 0:
            messagebox.showinfo("error", f"please input '{x}' correctly.")
            break
    with open('macro_cache.bin', 'wb') as f:
        pickle.dump(info, f)
    messagebox.showinfo('info', 'Done! Please relaunch this program again.')
    sys.exit()


if os.path.isfile('macro_cache.bin'):  # if user has cache file
    driver = webdriver.Chrome(ChromeDriverManager().install())  # installs ChromeDriver
    driver.get('https://www.discord.com/login/')  # login to discord
    driver.maximize_window()
    with open('macro_cache.bin', 'rb') as f:
        info = pickle.load(f)
    login_button = driver.find_element_by_xpath(
        '/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[1]/div/input')
    login_button.send_keys(info['email'])
    login_button = driver.find_element_by_xpath(
        '/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[2]/div/input')
    login_button.send_keys(info['pw'])
    login_button = driver.find_element_by_xpath(
        '/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/button[2]')
    login_button.click()  # login
    info1_label = Label(window, text="Delete \'macro_cache.bin\'")
    info1_label.grid(row=7, column=1)
    info2_label = Label(window, text="to reset login info.")
    info2_label.grid(row=8, column=1)
else:
    progress_label["text"] = "Type email and pw to login..."  # create cache file
    email_label = Label(window, text="email")
    email_label.grid(row=7, column=0)

    email_entry = Entry(window)
    email_entry.bind("<Return>", email_input)
    email_entry.grid(row=7, column=1)

    email_check = Label(window, text="ENTER", fg="red")
    email_check.grid(row=7, column=2)

    pw_label = Label(window, text="pw")
    pw_label.grid(row=8, column=0)

    pw_entry = Entry(window)
    pw_entry.bind("<Return>", pw_input)
    pw_entry.grid(row=8, column=1)

    pw_check = Label(window, text="ENTER", fg="red")
    pw_check.grid(row=8, column=2)

    start_button = Button(window, text="register", command=register)
    start_button.grid(row=9, column=1, sticky=W + E + N + S)


def content_input(event):
    """get content of message"""
    global content, check
    content = str(Entry.get(content_entry))
    content_check["text"] = "OK"
    content_check["fg"] = "green"
    check['content'] = 1


def count_input(event):
    """get counts of sending message"""
    global count, check
    try:
        count = int(Entry.get(count_entry))
    except ValueError:
        count_check["text"] = "ERROR"
        count_check["fg"] = "red"
        messagebox.showinfo("error", "type \'whole number\' only")
        check['count'] = 0
    else:
        count_check["text"] = "OK"
        count_check["fg"] = "green"
        check['count'] = 1


def interval_input(event):
    """get invertal for sending message"""
    global interval, check
    try:
        interval = float(Entry.get(interval_entry))
    except ValueError:
        interval_check["text"] = "ERROR"
        interval_check["fg"] = "red"
        messagebox.showinfo("error", "type \'demical number\' only")
        check['interval'] = 0
    else:
        interval_check["text"] = "OK"
        interval_check["fg"] = "green"
        check['interval'] = 1


def start_macro():
    """starts the macro"""
    global content, interval, count, check, progress_label, z
    for x, y in check.items():
        if y == 0:
            messagebox.showinfo("error", f"please input '{x}' correctly.")
            break

    try:
        discord = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/main/form/div/div/div/div/div[3]/div[2]')
    except NoSuchElementException:
        try:
            discord = driver.find_element_by_class_name('markup-2BOw-j slateTextArea-1Mkdgw fontSize16Padding-3Wk7zP')
        except NoSuchElementException:
            messagebox.showinfo("error", "Please login to discord and enter a channel.")
            return
    progress_label["text"] = "0%"

    for z in range(count):
        discord.send_keys(content)
        discord.send_keys(Keys.ENTER)
        time.sleep(interval)
    progress_label["text"] = "Macro completed!"
    driver.quit()
    messagebox.showinfo("info", "Done!")
    sys.exit()  # ends the program

# gui settings
window.title("Macro for discord")
window.geometry("310x300+100+100")
window.resizable(False, False)

content_label = Label(window, text="content")
content_label.grid(row=0, column=0)

content_entry = Entry(window)
content_entry.bind("<Return>", content_input)
content_entry.grid(row=0, column=1)

content_check = Label(window, text="ENTER", fg="red")
content_check.grid(row=0, column=2)

count_label = Label(window, text="count")
count_label.grid(row=1, column=0)

count_entry = Entry(window)
count_entry.bind("<Return>", count_input)
count_entry.grid(row=1, column=1)

count_check = Label(window, text="ENTER", fg="red")
count_check.grid(row=1, column=2)

interval_label = Label(window, text="interval")
interval_label.grid(row=2, column=0)

interval_entry = Entry(window)
interval_entry.bind("<Return>", interval_input)
interval_entry.grid(row=2, column=1)

interval_check = Label(window, text="ENTER", fg="red")
interval_check.grid(row=2, column=2)

start_button = Button(window, text="start macro", command=start_macro)
start_button.grid(row=3, column=1, sticky=W + E + N + S)

space1 = Label(window, text="ㅤ")
space1.grid(row=4, column=2)


space2 = Label(window, text="ㅤ")
space2.grid(row=6, column=2)


window.mainloop()  #thanks


