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

content = ">낚시 낚기"
count = 0
check2 = {'email': 0, 'pw': 0}
info = {'auto': 'wait'}
z = 0

window = Tk()


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
            messagebox.showinfo("오류", f"'{x}' 항목을 정확히 입력해 주세요.")
            break
    info['auto'] = 'y'
    with open('cache.bin', 'wb') as f:
        pickle.dump(info, f)
    messagebox.showinfo('안내', '완료! 프로그램을 재시작 후 사용해주시기 바랍니다.')
    sys.exit()


def no_auto():
    global check2
    info['auto'] = 'n'
    with open('cache.bin', 'wb') as f:
        pickle.dump(info, f)
    messagebox.showinfo('안내', '완료! 프로그램을 재시작 후 사용해주시기 바랍니다.')
    sys.exit()


if os.path.isfile('cache.bin'):  # if user has cache file
    driver = webdriver.Chrome(ChromeDriverManager().install())  # installs ChromeDriver
    driver.get('https://www.discord.com/login/')  # login to discord
    driver.maximize_window()

    info1_label = Label(window, text="로그인 정보를 수정하고")
    info1_label.grid(row=6, column=1)

    info2_label = Label(window, text="싶으시다면 'cache.bin'")
    info2_label.grid(row=7, column=1)

    info3_label = Label(window, text="파일을 삭제 해주세요.")
    info3_label.grid(row=8, column=1)

    with open('cache.bin', 'rb') as f:
        info = pickle.load(f)
    if info['auto'] == "y":
        login_button = driver.find_element_by_name("email")
        login_button.send_keys(info['email'])
        login_button = driver.find_element_by_name("password")
        login_button.send_keys(info['pw'])
        login_button = driver.find_element_by_xpath(
            '/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/button[2]')
        login_button.click()  # login
    elif info['auto'] == "n":
        messagebox.showinfo("정보", "디스코드에 로그인 해주세요.")
else:
    noauto_button = Button(window, text="자동로그인 사용 안함", command=no_auto)
    noauto_button.grid(row=9, column=1, sticky=W + E + N + S)

    email_label = Label(window, text="email")
    email_label.grid(row=6, column=0)

    email_entry = Entry(window)
    email_entry.bind("<Return>", email_input)
    email_entry.grid(row=6, column=1)

    email_check = Label(window, text="ENTER", fg="red")
    email_check.grid(row=6, column=2)

    pw_label = Label(window, text="pw")
    pw_label.grid(row=7, column=0)

    pw_entry = Entry(window)
    pw_entry.bind("<Return>", pw_input)
    pw_entry.grid(row=7, column=1)

    pw_check = Label(window, text="ENTER", fg="red")
    pw_check.grid(row=7, column=2)

    start_button = Button(window, text="register", command=register)
    start_button.grid(row=8, column=1, sticky=W + E + N + S)


def count_50():
    """get counts of sending message"""
    global count
    count = 50


def count_150():
    """get counts of sending message"""
    global count
    count = 150


def count_950():
    """get counts of sending message"""
    global count
    count = 950


def start_macro():
    """starts the macro"""
    global content, count

    try:
        discord = driver.find_element_by_css_selector(
            '#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div > div > div.chat-3bRxxu > div > main > form > div > div > div > div > div.textArea-12jD-V.textAreaSlate-1ZzRVj.slateContainer-3Qkn2x > div.markup-2BOw-j.slateTextArea-1Mkdgw.fontSize16Padding-3Wk7zP')
    except NoSuchElementException:
        messagebox.showinfo("오류", "디스코드에 로그인 후 유효한 채널에 접속해 주세요.")
        return

    for z in range(count):
        discord.send_keys(content)
        discord.send_keys(Keys.ENTER)
        time.sleep(0.5)
        if z % 10 == 0:
            discord.send_keys(">낚시 처분")
            discord.send_keys(Keys.ENTER)
        time.sleep(4)
    discord.send_keys(">낚시 팔기 일반")
    discord.send_keys(Keys.ENTER)
    time.sleep(5)
    discord.send_keys(">낚시 팔기 희귀")
    discord.send_keys(Keys.ENTER)
    time.sleep(5)
    discord.send_keys(">낚시 팔기 참치")
    discord.send_keys(Keys.ENTER)
    time.sleep(5)
    discord.send_keys(">낚시 팔기 복어")
    discord.send_keys(Keys.ENTER)
    time.sleep(5)
    discord.send_keys(">낚시 팔기 쓰레기")
    discord.send_keys(Keys.ENTER)
    time.sleep(5)
    discord.send_keys(">낚시 처분")
    discord.send_keys(Keys.ENTER)
    driver.quit()
    messagebox.showinfo("정보", "완료!")
    sys.exit()  # ends the program


# gui settings
window.title("Macro for codo-fishing")
window.geometry("310x300+100+100")
window.resizable(False, False)


zzap_button = Button(window, text="짭 낚시대", command=count_50)
zzap_button.grid(row=0, column=1, sticky=W + E + N + S)

normal_button = Button(window, text="일반 낚시대", command=count_150)
normal_button.grid(row=1, column=1, sticky=W + E + N + S)

good_button = Button(window, text="고급 낚시대", command=count_950)
good_button.grid(row=2, column=1, sticky=W + E + N + S)

space1 = Label(window, text="ㅤ")
space1.grid(row=3, column=2)

start_button = Button(window, text="start macro", command=start_macro)
start_button.grid(row=4, column=1, sticky=W + E + N + S)

space2 = Label(window, text="ㅤ")
space2.grid(row=5, column=2)

space3 = Label(window, text="ㅤㅤ   ㅤ            ㅤㅤㅤ")
space3.grid(row=0, column=0)

window.mainloop()  # thanks
