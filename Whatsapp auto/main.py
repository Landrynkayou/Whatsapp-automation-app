import pyautogui
from time import *
import datetime
import schedule
from model.db import Session, Message, ScheduledMessage

many=False
plural=False
alreadyEntered=0

def createMessage(contact, msg, time=""):
    session = Session()
    if time == "":
        time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%H:%M")
    # Create a new message
    new_message = Message(
        receiver = contact,
        content = msg,
        send_time = time
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
    # Use the Start menu search to open WhatsApp Desktop
    pyautogui.hotkey('win', 's')  # Open the Windows search menu
    sleep(1)
    pyautogui.write('WhatsApp', interval=0.1)  # Type WhatsApp
    sleep(1)
    pyautogui.press('enter')  # Open WhatsApp Desktop
    sleep(5)  # Allow time for the app to open

def sendMessages(contact, msg):
    global many, alreadyEntered
    print(f"[{datetime.datetime.now()}] Sending message to {contact}...")
    try:
        sleep(2)
        if (plural and many == False) or plural == False:
            print("Plural : ", plural)
            print("many : ", many)
            sleep(2)

            # Open WhatsApp Desktop
            print("Opening WhatsApp Desktop...")
            open_whatsapp_desktop()

            # Wait for WhatsApp to load
            while pyautogui.locateOnScreen('loading_chat.png'):
                print("Waiting for WhatsApp to load...")
                sleep(2)

            print("WhatsApp Desktop is ready!")
            sleep(2)
            many = True

        elif alreadyEntered > 0:
            pyautogui.click()
        else:
            alreadyEntered = alreadyEntered + 1
            pyautogui.click(pyautogui.locateOnScreen('reset_searchBar.png'))

        pyautogui.write(contact, interval=0.05)
        pyautogui.press('enter')
        pyautogui.write(msg, interval=0.2)
        print(f"[{datetime.datetime.now()}] Message sent!")
    except Exception as e:
        pyautogui.alert("The Automation process could not continue\nAn Error was encountered")
        print("Couldn't send the message", e)


def scheduleMessages():
    session = Session()  # Create a session
    now = datetime.datetime.utcnow()
    pending_messages = (
        session.query(Message)
        .all()
    )

    global plural
    if len(pending_messages) > 1:
        plural=True
    print("Len of message array :",len(pending_messages))
    for message in pending_messages:
        # Send the message
        scheduleTableVal = session.query(ScheduledMessage).filter(ScheduledMessage.message_id == message.id)
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



if __name__ == "__main__" :
    # sendMessages()
    createMessage("Yohan_auges","Hello")
    createMessage("Megane","Gracias")
    createMessage("Python","Testing connection with database\n","05:48")
    sleep(3)
    scheduleMessages()


