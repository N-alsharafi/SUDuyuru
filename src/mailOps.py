import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from time import sleep
from random import randint

import dbOps

#logging setup
import logging

logger = logging.getLogger(__name__)


def mail_process(email_add, email_pass, email_server, email_port, database):
    """This function will generate the necessary information and send an email
    it will also split the client list into groups of 9 and send them respective emails
    with a random wait time in-between to avoid triggering the spam filter"""
    
    #generate variables using functions
    announcements = dbOps.get_unsent_announcements(database)
    recievers_email = [client['email'] for client in dbOps.get_all_clients(database)]

    #split the recievers_email list into chunks of 9
    processed_recievers_email = [recievers_email[i:i+9] for i in range(0, len(recievers_email), 9)]
        #length set to 9 because 10 or more trips the filter

    body = mail_body(announcements)
    html_body = mail_html_body(announcements)


    #send message
    failed_emails = 0

    for recievers_group in processed_recievers_email:
        sent_successfully = send_mail(email_add, email_pass, email_server, email_port, recievers_group, body, html_body, len(announcements))
        if not sent_successfully:
            failed_emails += 1

        #wait a random amount of time between emails
        sleeptime = randint(3, 15)      #this stands to be adjusted
        sleep(sleeptime)
        logger.debug(f"Waiting {sleeptime} seconds before sending the next email")


    logger.info(f"Sent {len(processed_recievers_email) - failed_emails} email/s to {len(recievers_email)} reciever/s, {failed_emails} emails failed to send.")

    #mark announcements as sent if more than half the emails were sent successfully
    if(failed_emails < len(processed_recievers_email)/2):
        for announcement in announcements:
            dbOps.mark_as_sent(announcement, database)
        
        logger.info("Marked announcements as sent")
    else:
        logger.info("Did not mark announcements as sent due to too many failed emails")


def send_mail(email_add, email_pass, email_server, email_port, recievers_group, body, html_body, no_of_announcements):
    """This function will get the necessary mail sending information, a sublist of 
    processed_recievers_email and the mail object that already contains the email except msg['Bcc']
    Function will complete mail object, open a session and mail the email
    returns true if successful, false otherwise
    """
    #construct the mail object
    msg = EmailMessage()
    msg['Subject'] = f"{no_of_announcements} New Announcements!"
    msg['From'] = formataddr(('duyuruSU', email_add))  #it would be funny if this became duyuruSU
    msg['To'] = email_add
    msg['Bcc'] = ', '.join(recievers_group) # Convert list to comma-separated string

    msg.set_content(body)
    msg.add_alternative(html_body, subtype='html')

    #send message
    logger.debug(f"Starting to send email to {len(recievers_group)} reciever/s")


    """The random sleep functionality could probably be implemented without
    disconnecting from the server, but that's an problem for another day.
    """
    try:
        with smtplib.SMTP(email_server, email_port) as server:
            server.starttls()
            server.login(email_add, email_pass)
            server.send_message(msg)
            server.quit()
            logger.debug(f'Email sent to {len(recievers_group)} reciever/s')

        return True
    
    except:
        logger.error(f"Failed to send email to {len(recievers_group)} reciever/s")
        return False
    

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
