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
    send_time = Column(String, nullable=False)  # Default UTC time
    repition = Column(Boolean, nullable=True, default=False)

    scheduledMessage = relationship('ScheduledMessage', back_populates='message')


class ScheduledMessage(Base):
    __tablename__ = 'ScheduledMessages'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey('AutomatedMessages.id'), nullable=False)
    scheduled_time = Column(DateTime, default=lambda: (datetime.datetime.now() + datetime.timedelta(hours=1)), nullable=True)
    status = Column(String, default='In Process')

    message = relationship('Message', back_populates='scheduledMessage')



# Create tables
Base.metadata.create_all(engine)
print("Database and tables created successfully!")

# Initialize session
Session = sessionmaker(bind=engine)
session = Session()




