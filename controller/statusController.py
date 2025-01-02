import os
import pyautogui
from time import *
import datetime
import schedule
from model.db import Session, Message, ScheduledOperation

oppened = False



def post_whatsapp_status(content, text=""):
    global oppened
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
        if os.path.exists(content):
            pyautogui.hotkey('ctrl', 'l')
            sleep(1)
            pyautogui.write(content, interval=0.08) 
            pyautogui.press("enter")
            sleep(3)
            pyautogui.write(text, interval=0.08) 
        else:
            print("Status File path does not exist")
            return
                
        print("Posting status...")
        try:
            pyautogui.click(pyautogui.locateOnScreen("controller/image/postImg_button.png", confidence=0.8))
            print("Status posted successfully!")
        except Exception as e:
            print("Exception Caught : Post button not found.")
            raise

        print("Inside first try")
                
    except Exception as e:
        print("Exception Primary :An Error was encountered when posting the status : \n ")
        raise
        return
    finally:
        print("end")


if __name__ == "__main__" :
    # print(f"Current Working Directory: {os.getcwd()}")
    sleep(4)
    post_whatsapp_status("/home/hitechangel/Pictures/chat2.png", "My App")  # Update with the correct path
