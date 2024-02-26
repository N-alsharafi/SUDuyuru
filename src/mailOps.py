import smtplib
from email.message import EmailMessage
from email.utils import formataddr

import dbOps

#logging setup
import logging

logger = logging.getLogger(__name__)


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
        logger.info(f'Email sent to {len(recievers_email)} recievers')

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
    #CSS styling
    html_body = """\
    <html>
    <head>
        <style>
            body {
                background-color: #ffffff;
                font-family: Arial, sans-serif;
                text-align: center; /* Align everything to center */
            }
    
            h1 {
                color: #ffffff;
            }
    
            h2 {
                font-size: 1.6em;
                text-align: center; /* Reset text alignment for headings */
            }

            h3 {
                font-size: 1.3em;
                text-align: center; /* Reset text alignment for headings */
            }

            p {
                font-size: 1.1em;
                text-align: center; /* Reset text alignment for paragraphs */
            }
    
            table {
                width: 100%;
                font-size: 1.1em;
                border-collapse: collapse;
                text-align: left; /* Reset text alignment for table cells */
            }
    
            th, td {
                border: 0px solid #ddd;
                padding: 8px;
                text-align: left;
            }
    
            tr:nth-child(even) {
                background-color: #ffffff;
            }
            
            .top-bar {
                background-color: rgb(17, 17, 184);
                color: white;
                padding: 0px;
                text-align: left;
                text-indent: 20px;
                font-size: 1.5em;
            }
        </style>
    </head>
    """
    #HTML head
    html_body += f"""\
    <body>
    <div class="top-bar">
        <h1>SUDuyuru</h1>
    </div>
    <p>Hello,</p>
    <h2>There are <strong>{len(announcements)}</strong> new announcements!</h2>
    <table>
    """
    #HTML body
    for announcement in announcements:
        if announcement['new']:
            html_body += f"""\
            <tr>
                <td><a href="{announcement['link']}"><strong>{announcement['title']}</strong></a></td>
            </tr>
            """
        else:
            html_body += f"""\
            <tr>
                <td><a href="{announcement['link']}">{announcement['title']}</a></td>
            </tr>
            """
    #HTML foot
    html_body += """\
            </table>
            <br><br>
        </br>
            <p>
                <a href="https://mysu.sabanciuniv.edu/announcements/en/all">View all announcements</a>
            </br> or edit your preferences <a href="https://forms.gle/N8ys9iFqx2oKuKq29">here</a>.
            </p>
            <p>Best,<br>SUDuyuru team</p>
        </body>
    </html>
    """
    return html_body