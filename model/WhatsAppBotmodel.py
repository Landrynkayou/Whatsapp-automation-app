# Handles automation features like sending and scheduling messages.


# WhatsAppBot Model (Handles Automation)
class WhatsAppBot:
    def __init__(self):
        self.message_log = []

    def send_message(self, message):
        try:
            kit.sendwhatmsg_instantly(message.recipient.phone_number, message.content)
            self.message_log.append(message.get_message_info())
            print(f"Message sent to {message.recipient.phone_number}")
        except Exception as e:
            print("Error:", e)

    def schedule_message(self, message, hour, minute):
        try:
            kit.sendwhatmsg(message.recipient.phone_number, message.content, hour, minute)
            self.message_log.append(message.get_message_info())
            print(f"Message scheduled for {message.recipient.phone_number} at {hour}:{minute}")
        except Exception as e:
            print("Error:", e)

    def get_message_history(self):
        return self.message_log