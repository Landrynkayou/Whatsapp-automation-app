import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import threading
import schedule
from time import sleep

# Placeholder database
messages_db = []
scheduled_messages_db = []


# Functions for Message Handling
def create_message_gui(contact, msg, time):
    if not time:
        time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%H:%M")
    try:
        # Create a new message
        message_id = len(messages_db) + 1
        new_message = {
            'id': message_id,
            'receiver': contact,
            'content': msg,
            'send_time': time
        }
        messages_db.append(new_message)

        # Create scheduled message
        scheduled_message = {
            'message_id': message_id,
            'status': 'Pending'
        }
        scheduled_messages_db.append(scheduled_message)

        messagebox.showinfo("Success", "Message scheduled successfully!")
        update_message_list()
        update_status_dashboard()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to schedule message: {str(e)}")


def send_scheduled_messages():
    try:
        for message in messages_db:
            schedule.every().day.at(message['send_time']).do(
                send_message, contact=message['receiver'], msg=message['content']
            )
        messagebox.showinfo("Scheduler", "Scheduler started!")

        while True:
            schedule.run_pending()
            sleep(1)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start scheduler: {str(e)}")


def send_message(contact, msg):
    print(f"Sending message to {contact}: {msg}")
    # Update the status of the message
    for scheduled_message in scheduled_messages_db:
        if messages_db[scheduled_message['message_id'] - 1]['receiver'] == contact:
            scheduled_message['status'] = 'Completed'
    update_status_dashboard()


# New function to manually update status
def manual_update_status(contact, new_status):
    try:
        for scheduled_message in scheduled_messages_db:
            message = next((msg for msg in messages_db if msg['id'] == scheduled_message['message_id']), None)
            if message and message['receiver'] == contact:
                scheduled_message['status'] = new_status
                update_status_dashboard()
                messagebox.showinfo("Success", f"Status for {contact} updated to {new_status}!")
                return
        messagebox.showwarning("Warning", f"No message found for contact: {contact}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update status: {str(e)}")


# GUI Setup
def start_scheduler_thread():
    threading.Thread(target=send_scheduled_messages, daemon=True).start()


def update_message_list():
    # Clear current list
    for row in message_tree.get_children():
        message_tree.delete(row)

    for message in messages_db:
        status = next((sm['status'] for sm in scheduled_messages_db if sm['message_id'] == message['id']), 'Unknown')
        message_tree.insert("", "end", values=(message['receiver'], message['content'], message['send_time'], status))


def update_status_dashboard():
    # Clear current status dashboard
    for row in status_tree.get_children():
        status_tree.delete(row)

    for scheduled_message in scheduled_messages_db:
        message = next((msg for msg in messages_db if msg['id'] == scheduled_message['message_id']), None)
        if message:
            status_tree.insert("", "end", values=(message['receiver'], scheduled_message['status']))


# Main GUI
root = tk.Tk()
root.title("Message Scheduler GUI")
root.geometry("1200x700")
root.configure(bg="#f0f8ff")  # Light blue background

# Styles
style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 12), rowheight=30)
style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="#4682b4", foreground="white")
style.configure("TButton", font=("Helvetica", 12), padding=10)

# Input Fields
input_frame = tk.Frame(root, bg="#f0f8ff")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Contact:", font=("Helvetica", 14), bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5,
                                                                                  sticky='e')
contact_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=30)
contact_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Message:", font=("Helvetica", 14), bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=5,
                                                                                  sticky='e')
message_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=30)
message_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Time (HH:MM):", font=("Helvetica", 14), bg="#f0f8ff").grid(row=2, column=0, padx=5, pady=5,
                                                                                       sticky='e')
time_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=30)
time_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
button_frame = tk.Frame(root, bg="#f0f8ff")
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Send Now",
           command=lambda: create_message_gui(contact_entry.get(), message_entry.get(), "")) \
    .grid(row=0, column=0, padx=10, pady=10)

ttk.Button(button_frame, text="Schedule",
           command=lambda: create_message_gui(contact_entry.get(), message_entry.get(), time_entry.get())) \
    .grid(row=0, column=1, padx=10, pady=10)

ttk.Button(button_frame, text="Start Scheduler", command=start_scheduler_thread) \
    .grid(row=0, column=2, padx=10, pady=10)

# Manual Status Update Fields
status_update_frame = tk.Frame(root, bg="#f0f8ff")
status_update_frame.pack(pady=10)

tk.Label(status_update_frame, text="Update Status for Contact:", font=("Helvetica", 14), bg="#f0f8ff").grid(row=0,
                                                                                                            column=0,
                                                                                                            padx=5,
                                                                                                            pady=5,
                                                                                                            sticky='e')
status_contact_entry = tk.Entry(status_update_frame, font=("Helvetica", 14), width=30)
status_contact_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(status_update_frame, text="New Status:", font=("Helvetica", 14), bg="#f0f8ff").grid(row=1, column=0, padx=5,
                                                                                             pady=5, sticky='e')
new_status_entry = tk.Entry(status_update_frame, font=("Helvetica", 14), width=30)
new_status_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(status_update_frame, text="Update Status",
           command=lambda: manual_update_status(status_contact_entry.get(), new_status_entry.get())) \
    .grid(row=2, column=0, columnspan=2, pady=10)

# Message List
list_frame = tk.Frame(root, bg="#f0f8ff")
list_frame.pack(pady=10)

columns = ("Contact", "Message", "Time", "Status")
message_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
for col in columns:
    message_tree.heading(col, text=col)
    message_tree.column(col, width=180, anchor="center")

message_tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Status Dashboard
status_frame = tk.Frame(root, bg="#f0f8ff")
status_frame.pack(pady=10)

tk.Label(status_frame, text="Status Dashboard", font=("Helvetica", 16, "bold"), bg="#f0f8ff") \
    .pack(pady=5)

status_columns = ("Contact", "Status")
status_tree = ttk.Treeview(status_frame, columns=status_columns, show="headings")
for col in status_columns:
    status_tree.heading(col, text=col)
    status_tree.column(col, width=300, anchor="center")

status_tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

update_message_list()
update_status_dashboard()

root.mainloop()
