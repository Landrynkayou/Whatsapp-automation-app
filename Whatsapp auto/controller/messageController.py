import pyautogui
from time import *
import datetime
import schedule
from model.db import Session, Message, ScheduledMessage

many = False
plural = False
alreadyEntered = 0

def createMessage(contact, msg, time=""):
    session = Session()
    if time == "":
        time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%H:%M")
    # Create a new message
    new_message = Message(
        receiver=contact,
        content=msg,
        send_time=time
    )
    session.add(new_message)
    session.commit()

    # Schedule the message
    scheduled_message = ScheduledMessage(
        message_id=new_message.id,
    )
    session.add(scheduled_message)
    session.commit()

    print("Message and scheduled message added successfully!")

def open_whatsapp_desktop():
    print("Opening WhatsApp Desktop...")
    pyautogui.hotkey("win", "s")  # Open search bar
    sleep(1)
    pyautogui.write("WhatsApp", interval=0.1)  # Type WhatsApp
    pyautogui.press("enter")  # Open WhatsApp Desktop
    sleep(5)  # Wait for WhatsApp Desktop to open

def sendMessages(contact, msg):
    global many, alreadyEntered
    print(f"[{datetime.datetime.now()}] Sending message to {contact}...")
    try:
        if (plural and not many) or not plural:
            print("Plural : ", plural)
            print("many : ", many)
            open_whatsapp_desktop()
            sleep(3)

            while pyautogui.locateOnScreen('controller/image/loading_bar1.png') or pyautogui.locateOnScreen('controller/image/loading_bar2.png'):
                print("Waiting for WhatsApp to load...")
                sleep(3)

            print("WhatsApp is ready.")
            sleep(3)

            pyautogui.click(pyautogui.locateOnScreen('controller/image/search_icon.png'))
            many = True
        else:
            alreadyEntered += 1
            pyautogui.click(pyautogui.locateOnScreen('controller/image/reset_searchBar.png'))

        pyautogui.write(contact, interval=0.05)  # Type contact name
        pyautogui.press('enter')  # Select contact
        sleep(1)
        pyautogui.write(msg, interval=0.2)  # Type message
        pyautogui.press('enter')  # Send message
        print(f"[{datetime.datetime.now()}] Message sent!")
    except Exception as e:
        pyautogui.alert("The Automation process could not continue\nAn Error was encountered.")
        print(f"Couldn't send the message to {contact}: ", e)

def scheduleMessages():
    session = Session()  # Create a session
    now = datetime.datetime.utcnow()
    pending_messages = (
        session.query(Message).all()
    )

    global plural
    if len(pending_messages) > 1:
        plural = True
    print("Len of message array :", len(pending_messages))

    for message in pending_messages:
        # Send the message
        scheduleTableVal = session.query(ScheduledMessage).filter(ScheduledMessage.message_id == message.id).first()
        sendTime = message.send_time
        schedule.every().day.at(sendTime).do(
            sendMessages,
            contact=message.receiver,
            msg=message.content
        )

        # Update the status in the database
        scheduleTableVal.status = 'Completed'
        session.commit()

    print("Scheduler is running. Waiting to send messages...\n\n")
    while True:
        schedule.run_pending()
        sleep(1)

if __name__ == "__main__":
    createMessage("Yohan_auges", "Hello")
    createMessage("Megane", "Gracias")
    createMessage("Python", "Testing connection with database\n", "05:48")
    sleep(3)
    scheduleMessages()
