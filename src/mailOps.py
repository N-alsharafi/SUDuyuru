import smtplib
from email.message import EmailMessage
from email.utils import formataddr

import creds #remove this later
import dbOps


def send_mail(email_add, email_pass, email_server, email_port, database):
    """This function will generate the necessary information and send an email"""
    #generate variables using functions
    announcements = dbOps.get_unsent_announcements(database)
    recievers_email = [client['email'] for client in dbOps.get_all_clients(database)]

    #email message
    msg = EmailMessage()
    msg['Subject'] = f"{len(announcements)} New Announcements!"
    msg['From'] = formataddr(('SU Duyuru', email_add))
    msg['To'] = email_add
    msg['Bcc'] = ', '.join(recievers_email) # Convert list to comma-separated string

    body = mail_body(announcements)
    html_body = mail_html_body(announcements)

    msg.set_content(body)
    msg.add_alternative(html_body, subtype='html')

    #send message
    with smtplib.SMTP(email_server, email_port) as server:
        server.starttls()
        server.login(email_add, email_pass)
        server.send_message(msg)
        server.quit()
        print(f'Email sent to {len(recievers_email)} recievers')

    for announcement in announcements:
        dbOps.mark_as_sent(announcement, database) #mark as sent


def mail_body(announcements):
    """This function will generate the body of the email"""
    body = f"Hello, \n\nThere are {len(announcements)} new announcements!\n\n"
    for announcement in announcements:
        body += f"{announcement['title']} \n{announcement['link']}\n\n"
    body += "Best,\nSUDuyuru team"
    return body


def mail_html_body(announcements):
    """This function will generate the html body of the email"""
    html_body = f"""\
    <html>
        <body>
            <p>Hello,</p>
            <p>There are <strong>{len(announcements)}</strong> new announcements!</p>
            """
    for announcement in announcements:
        if announcement['new']:
            html_body += f"""\
            <p><a href="{announcement['link']}"><strong>{announcement['title']}</strong></a></p>
            """
        else:
            html_body += f"""\
                <p><a href="{announcement['link']}">{announcement['title']}</a></p>
                """
    #add view all announcements link
    html_body += """\
            <br>
            <p><a href="https://mysu.sabanciuniv.edu/announcements/en/all">View all announcements</a></p>
            <p>Best,<br>SUDuyuru team</p>
        </body>
    </html>
    """
    return html_body