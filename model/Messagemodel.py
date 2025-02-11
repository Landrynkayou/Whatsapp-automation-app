# Manages message content, timestamps, and recipients.

# Message Model
class Message:
    def __init__(self, sender, recipient, content):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    def get_message_info(self):
        return {
            "sender": self.sender.phone_number,
            "recipient": self.recipient.phone_number,
            "content": self.content,
            "timestamp": self.timestamp
        }