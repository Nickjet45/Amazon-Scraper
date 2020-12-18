import smtplib

from smtplib import SMTP

def Send_Email(email, subject_msg, body_msg):
    try:
        print('Connecting to server')
        server: SMTP = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        print('Logining in to server')

        server.login("Email", 'App password')

        print("Successfully logged in")

        subject = subject_msg
        body = body_msg
        msg = f'subject: {subject} \n \n {body}'

        server.sendmail('Email', 
        email, 
        msg)

        print("Email has successfully been sent to {}".format(email))

    except Exception as e:
        print(e)
    
    finally:
        server.quit()


if __name__ == "__main__":
    pass

Send_Email('Email to send to', 'hi', 'bye')