from flask import current_app, render_template
from app.email import send_email

def send_reminder_email(reminder):
    print(f"Sending email for reminder {reminder}...")
    task = reminder.task
    user = task.owner
    send_email(subject = f"Reminder for task '{task.name}'", 
               sender = current_app.config['MAIL_FROM'],
               recipients = [user.email],
               html_body = render_template('mail/reminder.html',
                                           user=user, task=task, reminder=reminder),
               text_body = render_template('mail/reminder.txt',
                                           user=user, task=task, reminder=reminder),
              )
               

