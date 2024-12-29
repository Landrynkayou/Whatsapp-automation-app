from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import datetime

# Database setup
DATABASE_URI = 'sqlite:///model/whatsapp_automation.db'
engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()


# Define the tables (models)
class Message(Base):
    __tablename__ = 'AutomatedMessages'
    id = Column(Integer, primary_key=True)
    receiver = Column(String, nullable=False)
    content = Column(String, nullable=False)
    send_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)  # Default UTC time
    repetition = Column(Boolean, nullable=True, default=False)  # Fixed typo from 'repition'

    scheduled_message = relationship('ScheduledMessage', back_populates='message', uselist=False)

    def __repr__(self):
        return f"<Message(id={self.id}, receiver='{self.receiver}', send_time='{self.send_time}')>"


class ScheduledMessage(Base):
    __tablename__ = 'ScheduledMessages'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey('AutomatedMessages.id'), nullable=False)
    scheduled_time = Column(DateTime, default=lambda: datetime.datetime.utcnow() + datetime.timedelta(hours=1))
    status = Column(String, default='In Process')

    message = relationship('Message', back_populates='scheduled_message')

    def __repr__(self):
        return f"<ScheduledMessage(id={self.id}, scheduled_time='{self.scheduled_time}', status='{self.status}')>"


# Create tables
Base.metadata.create_all(engine)
print("Database and tables created successfully!")

# Initialize session
Session = sessionmaker(bind=engine)
session = Session()
