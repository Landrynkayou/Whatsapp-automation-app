from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import datetime

# Database setup
DATABASE_URI = 'sqlite:///whatsapp_automation.db'
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

    # scheduledOperation = relationship('ScheduledOperation', back_populates='message')

class Status(Base):
    __tablename__ = 'AutomatedStatus'
    id = Column(Integer, primary_key=True)
    media = Column(Boolean, nullable=False)
    content_or_path = Column(String, nullable=False)
    mediaText = Column(String, nullable=False, default="")
    send_time = Column(String, nullable=False)  # Default UTC time

    # scheduledOperation = relationship('ScheduledOperation', back_populates='message')

class ScheduledOperation(Base):
    __tablename__ = 'ScheduledOperation'
    id = Column(Integer, primary_key=True)
    operation = Column(String, nullable=False, default = "message")
    message_id = Column(Integer, ForeignKey('AutomatedMessages.id'), default=0)
    status_id = Column(Integer, ForeignKey('AutomatedStatus.id'), default=0)
    scheduled_time = Column(DateTime, default=lambda: (datetime.datetime.now() + datetime.timedelta(hours=0)), nullable=True)
    current_status = Column(String, default="In Process")

    message = relationship('Message', foreign_keys=[message_id])
    status = relationship('Status', foreign_keys=[status_id])



# Create tables
Base.metadata.create_all(engine)
print("Database and tables created successfully!")

# Initialize session
Session = sessionmaker(bind=engine)
session = Session()




