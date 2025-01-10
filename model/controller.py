from sqlalchemy.orm import Session
from sqlalchemy import update, delete
from db import Message, StatusLog, ScheduledMessage  # Assuming your models are saved in a file named models.py
import datetime

class DatabaseController:
    def __init__(self, session: Session):
        self.session = session

    # Message-related operations
    def create_message(self, recipient, content, send_time=None, status='pending'):
        message = Message(
            recipient=recipient,
            content=content,
            send_time=send_time or datetime.datetime.now(datetime.timezone.utc),
            status=status
        )
        self.session.add(message)
        self.session.commit()
        return message

    def get_all_messages(self):
        return self.session.query(Message).all()

    def update_message(self, message_id, **kwargs):
        self.session.execute(update(Message).where(Message.id == message_id).values(**kwargs))
        self.session.commit()

    def delete_message(self, message_id):
        self.session.execute(delete(Message).where(Message.id == message_id))
        self.session.commit()

    # StatusLog-related operations
    def create_status_log(self, content, post_time=None, status='pending'):
        status_log = StatusLog(
            content=content,
            post_time=post_time or datetime.datetime.now(datetime.timezone.utc),
            status=status
        )
        self.session.add(status_log)
        self.session.commit()
        return status_log

    def get_all_status_logs(self):
        return self.session.query(StatusLog).all()

    def update_status_log(self, log_id, **kwargs):
        self.session.execute(update(StatusLog).where(StatusLog.id == log_id).values(**kwargs))
        self.session.commit()

    def delete_status_log(self, log_id):
        self.session.execute(delete(StatusLog).where(StatusLog.id == log_id))
        self.session.commit()

    # ScheduledMessage-related operations
    def create_scheduled_message(self, recipient, content, scheduled_time, status='scheduled'):
        scheduled_message = ScheduledMessage(
            recipient=recipient,
            content=content,
            scheduled_time=scheduled_time,
            status=status
        )
        self.session.add(scheduled_message)
        self.session.commit()
        return scheduled_message

    def get_all_scheduled_messages(self):
        return self.session.query(ScheduledMessage).all()

    def update_scheduled_message(self, message_id, **kwargs):
        self.session.execute(update(ScheduledMessage).where(ScheduledMessage.id == message_id).values(**kwargs))
        self.session.commit()

    def delete_scheduled_message(self, message_id):
        self.session.execute(delete(ScheduledMessage).where(ScheduledMessage.id == message_id))
        self.session.commit()
