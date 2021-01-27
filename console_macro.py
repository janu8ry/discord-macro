import pickle
import os

import asyncio
from pyppeteer import launch
from pyppeteer.errors import TimeoutError, PageError

# selectors
LOGIN_EMAIL = '#app-mount > div.app-1q1i1E > div > div.leftSplit-1qOwnR.nonEmbeddedLeftSplit-3z6mge > div > div > form > div > div > div.mainLoginContainer-1ddwnR > div.block-egJnc0.marginTop20-3TxNs6 > div.marginBottom20-32qID7 > div > div.inputWrapper-31_8H8.inputWrapper-3aw2Sf > input'
LOGIN_PW = '#app-mount > div.app-1q1i1E > div > div.leftSplit-1qOwnR.nonEmbeddedLeftSplit-3z6mge > div > div > form > div > div > div.mainLoginContainer-1ddwnR > div.block-egJnc0.marginTop20-3TxNs6 > div:nth-child(2) > div > input'
LOGIN_BUTTON = '#app-mount > div.app-1q1i1E > div > div.leftSplit-1qOwnR.nonEmbeddedLeftSplit-3z6mge > div > div > form > div > div > div.mainLoginContainer-1ddwnR > div.block-egJnc0.marginTop20-3TxNs6 > button.marginBottom8-AtZOdT.button-3k0cO7.button-38aScr.lookFilled-1Gx00P.colorBrand-3pXr91.sizeLarge-1vSeWK.fullWidth-1orjjo.grow-q77ONN'
LOGIN_2FA = '#app-mount > div.app-1q1i1E > div > div.leftSplit-1qOwnR.nonEmbeddedLeftSplit-3z6mge > div > form > div > div.block-egJnc0.marginTop40-i-78cZ > div > div > input'
DISCORD_MAIN = '#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div > div > div.container-1D34oG > section > div.children-19S4PO > div.iconWrapper-2OrFZ1 > svg > g > path:nth-child(1)'
DISCORD_SEND = '#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div > div > div.chat-3bRxxu > div > main > form > div > div > div > div > div.textArea-12jD-V.textAreaSlate-1ZzRVj.slateContainer-3Qkn2x > div.markup-2BOw-j.slateTextArea-1Mkdgw.fontSize16Padding-3Wk7zP'


async def main():
    # gets login info
    if not os.path.isfile('cache.bin'):
        email = input("Please enter the email of your discord account.\n> ")
        pw = input("Please enter the password of your discord account.\n> ")
        with open('cache.bin', 'wb') as file:
            pickle.dump({'email': email, 'pw': pw}, file)
        print("login info safely stored.")

    # gets content
    while True:
        content = input("Message Content\n> ")
        try:
            assert len(content) <= 2000
            break
        except AssertionError:
            print("Please enter a content that has less than 2000 characters.")
            continue

    # gets interval
    while True:
        interval = input("Message Send Interval\n> ")
        try:
            interval = float(interval)
            break
        except ValueError:
            print("Error: Please enter an decimal number.")
            continue

    # gets count
    while True:
        count = input("Number of messages to send\n> ")
        try:
            count = int(count)
            break
        except ValueError:
            print("Error: Please enter an integer.")
            continue

    # gets server(guild) id
    while True:
        guild_id = input("target server(guild) id\n> ")
        try:
            guild_id = int(guild_id)
            assert len(str(guild_id)) == 18
            break
        except (ValueError, AssertionError) as e:  # noqa
            print("Please enter an 18-digit integer.")
            continue

    # gets channel id
    while True:
        channel_id = input("target channel id\n> ")
        try:
            channel_id = int(channel_id)
            assert len(str(channel_id)) == 18
            break
        except (ValueError, AssertionError) as e:  # noqa
            print("Please enter an 18-digit integer.")
            continue

    # launch pyppeteer
    browser = await launch(headless=False)
    page = await browser.newPage()

    # login to discord
    await page.goto('https://discord.com/login')
    await page.waitForSelector(LOGIN_EMAIL)
    with open('cache.bin', 'rb') as f:
        login_info = pickle.load(f)
    await page.focus(LOGIN_EMAIL)
    await page.keyboard.type(login_info['email'])
    await page.focus(LOGIN_PW)
    await page.keyboard.type(login_info['pw'])
    await page.click(LOGIN_BUTTON)
    try:
        await page.waitForSelector(DISCORD_MAIN, {'timeout': 10000})  # Wait for successful login
    except TimeoutError:
        try:  # if user uses 2fa
            await page.focus(LOGIN_2FA)
            while True:
                code = input("2FA code\n> ")
                try:
                    assert len(code) == 6
                    break
                except AssertionError:
                    print("Please enter an 6-digit integer(code).")
                    continue
            await page.keyboard.type(code)
            await page.keyboard.press('Enter')
            await page.waitForSelector(DISCORD_MAIN)
        except (TimeoutError, PageError) as f:  # captcha
            print("Error while logging in to discord...\nYour email/password is wrong or logged in an another region.", f)
            await browser.close()
            return

    # goes to target channel
    await page.goto(f"https://discord.com/channels/{guild_id}/{channel_id}")
    try:
        await page.waitForSelector(DISCORD_SEND)
    except TimeoutError:  # if the server(guild) or channel dosent exist or has no permissions
        print("Error: invalid server(guild)/channel id")
        await browser.close()
        return

    await page.focus(DISCORD_SEND)  # selects the input window
    for i in range(count):
        await page.keyboard.type(content)
        await page.keyboard.press('Enter')
        await asyncio.sleep(interval)
    print("Done!")  # macro done!
    await browser.close()


if __name__ == '__main__':
    print(
        '''       Macro for Discord v2.0
---------------------------------------
made by https://github.com/janu8ry
source - https://github.com/janu8ry/discord-macro
license - gpl 3.0

Chromium installation on the first run,and may cause slow operation.
---------------------------------------
''')
    asyncio.get_event_loop().run_until_complete(main())
