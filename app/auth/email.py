from flask import current_app, render_template
from app.email import send_email

def send_password_reset_email(user):
    print("Sending password reset email to user",user.username)
    token = user.generate_token()
    send_email(subject = 'Reset your password', 
               sender = current_app.config['MAIL_FROM'],
               recipients = [user.email],
               html_body = render_template('mail/reset_password.html',
                                           user=user, token=token),
               text_body = render_template('mail/reset_password.txt',
                                           user=user, token=token),
              )
               
