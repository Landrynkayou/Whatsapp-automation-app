import os
import pyautogui
from time import *
import datetime
import schedule
from model.db import Session, Status, ScheduledOperation

oppened = False

def createStatus(content, media=True, text="", time=""):
    session = Session()
    if time == "":
        time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%H:%M")
    # Create a new status
    new_status = Status(
        content_or_path = content,
        send_time = time,
        mediaText = text,
        media = media,
    )
    session.add(new_status)
    session.commit()

    # Schedule the status
    scheduled_status = ScheduledOperation(
        status_id=new_status.id,
    )
    session.add(scheduled_status)
    session.commit()

    print("status and scheduled status added successfully!")

def postStatus(content, text, media):
    global oppened
    sleep(2)
    try:
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
            print("WhatsApp Not Openned from exception")
            if oppened == False :
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
                while pyautogui.locateCenterOnScreen('controller/image/loading_bar1.png', confidence=0.7) and pyautogui.locateCenterOnScreen('controller/image/loading_bar2.png', confidence=0.7) :
                    print("Inside Loop 2")
                    sleep(3)
                    break
                sleep(4)
                print("Outside Loop")
            else :
                raise

        sleep(5)
        try :
            pyautogui.click(pyautogui.locateCenterOnScreen("controller/image/status_read.png", confidence=0.8))
        except Exception as e:
            print("Exception Caught : Couldn't found the status_read image")
            try :
                pyautogui.click(pyautogui.locateCenterOnScreen("controller/image/status_select.png", confidence=0.8))
            except Exception as e:
                print("Exception Caught : Couldn't found the status_select image")
                try :
                    pyautogui.click(pyautogui.locateCenterOnScreen("controller/image/status_unread.png", confidence=0.8))
                except Exception as e:
                    print("Exception Caught : Couldn't found the status_unread image")
                    raise
        
        sleep(1)
        pyautogui.click(pyautogui.locateCenterOnScreen("controller/image/status_add.png", confidence=0.8))
        pyautogui.press("down")
        # pyautogui.press("down")
        pyautogui.press("enter")
        print("Navigating file explorer...")
        if media == True:
            if os.path.exists(content):
                pyautogui.hotkey('ctrl', 'l')
                sleep(1)
                pyautogui.write(content, interval=0.08) 
                pyautogui.press("enter")
                sleep(3)
                pyautogui.write(text, interval=0.08) 
            else:
                print("Status File path does not exist")
                raise
                return
        else:
            sleep(1)
            pyautogui.write(content, interval=0.08) 
                
        print("Posting status...")
        try:
            pyautogui.click(pyautogui.locateOnScreen("controller/image/postImg_button.png", confidence=0.8))
            print("Status posted successfully!")
        except Exception as e:
            print("Exception Caught : Post button not found.")
            raise

        print("Inside first try")
                
    except Exception as e:
        pyautogui.alert("The Automation process could not continue\nAn Error was encountered ")
        print("Exception Primary :An Error was encountered when posting the status : \n ")
        raise
        return

def scheduleStatus():
    session = Session()  # Create a session
    now = datetime.datetime.utcnow()
    pending_status = (
        session.query(Status)
        .all()
    )

    for status in pending_status:
        # Send the Status
        scheduleTableVal = session.query(ScheduledOperation).filter(ScheduledOperation.status_id == status.id)
        sendTime = status.send_time
        schedule.every().day.at(sendTime).do(
            postStatus,
            content=status.content_or_path,
            text=status.mediaText,
            media=status.media
        )

        # Update the status in the database
        scheduleTableVal.status = 'Completed'
        session.commit()

    print("Scheduler is running. Waiting to post Status...\n\n")
    while True:
        schedule.run_pending()
        sleep(1)

