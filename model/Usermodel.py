# Represents a WhatsApp user.

import time
import pywhatkit as kit

# User Model
class User:
    def __init__(self, phone_number, name="Unknown"):
        self.phone_number = phone_number
        self.name = name
    
    def get_details(self):
        return {"name": self.name, "phone": self.phone_number}





# ✅ Example Usage
if __name__ == "__main__":
    user1 = User("+237600000000", "Alice")
    user2 = User("+237700000000", "Bob")

    msg = Message(user1, user2, "Hello Bob! This is an automated message.")
    
    bot = WhatsAppBot()
    bot.send_message(msg)
    print("Message History:", bot.get_message_history())
