from app import scheduler, db
from app.models import Reminder
from app.main.email import send_reminder_email
from datetime import datetime

@scheduler.task("interval", id="send_reminders", seconds=20)
def send_reminders():
    with db.app.app_context():
        if db.app.config['MAIL_ENABLED']:
            for reminder in Reminder.query.filter(
                Reminder.sent == False,
                Reminder.time < datetime.utcnow()
            ):
                send_reminder_email(reminder)
                reminder.sent=True
                db.session.commit()
