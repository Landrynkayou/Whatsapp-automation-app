import pyautogui
from time import *
import datetime
import schedule
from model.db import Session, Message, ScheduledOperation
from utils.oppenZapp import *

oppened=False # serve as a flag to determine if whatsapp is already oppened or not

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
    scheduled_message = ScheduledOperation(
        message_id=new_message.id,
    )
    session.add(scheduled_message)
    session.commit()

    print("Message and scheduled message added successfully!")


def sendMessages(contact, msg):
    global oppened
    print(f"[{datetime.datetime.now()}] Sending message to {contact}...")
    try:
        sleep(2)
        try:
            try :
                pyautogui.locateCenterOnScreen("controller/image/chat_open.png", confidence=0.8)
                oppened = True
            except Exception as e:
                try :
                    pyautogui.click(pyautogui.locateCenterOnScreen("controller/image/channel_open.png", confidence=0.8))
                    oppened = True
                except Exception as e:
                    try :
                        pyautogui.click(pyautogui.locateCenterOnScreen("controller/image/status_open.png", confidence=0.8))
                        oppened = True
                    except Exception as e:
                        try :
                            pyautogui.click(pyautogui.locateCenterOnScreen("controller/image/community_open.png", confidence=0.8))
                            oppened = True
                        except Exception as e:
                            print("WhatsApp Isn't Openned")
                            raise
        except Exception as e:
            oppened = False
        
        if oppened==False :
            print("oppened : ",oppened)
            sleep(2)
            pyautogui.click(x=380, y=13) 
            sleep(2)
            pyautogui.hotkey("win", "up")
            sleep(0.5)
            pyautogui.click(x=450, y=100) 
            # pyautogui.click(x=1200, y=95) 
            pyautogui.write('https://web.whatsapp.com/\n', interval=0.08) 
            # sleep(7)
            sleep(4)
            print("Before Loop")
            try:
                pyautogui.locateCenterOnScreen('controller/image/loading_chat.png', confidence=0.7)
                print("Whatsapp is loading chats .............................")
                while pyautogui.locateCenterOnScreen('controller/image/loading_chat.png', confidence=0.7) :
                    sleep(1)
            except Exception as e:
                print("Chat Loaded !!!!!!!")
            print("hi")
            sleep(2)
            try:
                while pyautogui.locateCenterOnScreen('controller/image/loading_bar1.png', confidence=0.7) :
                    sleep(1)
            except Exception as e:
                try:
                    while pyautogui.locateCenterOnScreen('controller/image/loading_bar2.png', confidence=0.7) :
                        sleep(1)
                except Exception as e:
                    raise
            print("hi2")
        
            sleep(5)
            print("Outside Loop")
            sleep(3)
        
            pyautogui.click(pyautogui.locateOnScreen('controller/image/search_icon.png', confidence=0.8))
        else:
            pyautogui.click(pyautogui.locateOnScreen('controller/image/reset_seachBar.png', confidence=0.8))

        pyautogui.write(contact, interval=0.05) 
        pyautogui.press('enter')
        pyautogui.write(msg, interval=0.2)
        print(f"[{datetime.datetime.now()}] Message sent!")
    except Exception as e:
        pyautogui.alert("The Automation process could not continue\nAn Error was encountered\n !! Verify your Internet connection !!")
        print("Couldn't send the message to "+contact+" : ",e)

def scheduleMessages():
    session = Session()  # Create a session
    now = datetime.datetime.utcnow()
    pending_messages = (
        session.query(Message)
        .all()
    )

    print("Len of message array :",len(pending_messages))
    for message in pending_messages:
        # Send the message
        scheduleTableVal = session.query(ScheduledOperation).filter(ScheduledOperation.message_id == message.id)
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


