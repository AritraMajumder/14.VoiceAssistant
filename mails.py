import requests
import json
import re
from keys import *
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def summarizer(text):
    clean_text = text.replace("\r\n", "")
    headers = {"Authorization": "Bearer "+eden_key}
    url ="https://api.edenai.run/v2/text/summarize"
    payload={"providers": "microsoft,connexun,openai", "language": "en", "text": clean_text}
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    return result['microsoft']['result']

def extract_email_body(msg):
    if msg.is_multipart():
        for part in msg.get_payload():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()

def generator(prompt,name):
    headers = {"Authorization": "Bearer "+eden_key}

    url = "https://api.edenai.run/v2/text/generation"
    payload = {
        "providers": "openai,cohere",
        "text": prompt+ " to " + name + "from YOUR_NAME",
        "temperature": 0.2,
        "max_tokens": 250
    }
    response = requests.post(url,json=payload,headers=headers)
    result = json.loads(response.text)
    return result['openai']['generated_text']

def mailer(name,subject,prompt):
    #you can mail from a single preset email address to your contacts
    contacts = {'person1':'mail1',
                'person2':'mail2'
                }
    body = generator(prompt,name)
    #hard coded
    sender_email = 'your mail id'
    username = 'your mail id'
    if name not in contacts:
        return 2
    receiver_email = contacts[name]
    sub = subject
    message = body
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    password = mail_key

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = sub
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Create a SMTP session
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()  
            server.starttls()  
            server.login(username, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            return body
    except Exception as e:
        return 0

def reader(num,option):
    mails = []
    tasks = []
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        result = imap.login('your mail id', mail_key)
        imap.select('inbox',readonly = True)
        response, messages = imap.search(None,'ALL')
        messages = messages[0].split()
        latest = int(messages[-1])
        #oldest = int(messages[0])
        for i in range(latest, latest-num, -1):
            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # Assuming `msg` is an email.message.Message object
                    msg = email.message_from_bytes(response[1])
                    # print required information
                    time = msg["Date"].split(" ")[:-1]
                    time = " ".join(time)[:-3]
                    sender = msg["From"].split(" ")[0]
                    body = extract_email_body(msg)
                    tasks.append(body)
                    body = summarizer(body)
                    mails.append([time,sender,body])
        if option==1:          
            return mails
        elif option==2:
            task_list = tasker(tasks)
            return task_list
    except Exception as e:
        return 0     

def tasker(body):
    headers = {"Authorization": "Bearer "+eden_key}
    url ="https://api.edenai.run/v2/text/question_answer"
    listed = []
    for i in body:
        i = i.replace("\r\n", "")
        pattern = r'[^a-zA-Z0-9\s]'
        i = re.sub(pattern, '', i)
        payload={"providers": "openai", "texts": [i],'question':"what are the tasks given here?", "examples_context":"In 2017, U.S. life expectancy was 78.6 years.", "examples":[["What is human life expectancy in the United States?", "78 years."],]}
        response = requests.post(url, json=payload, headers=headers)
        result = json.loads(response.text)
        listed.append(result['openai']['answers'])
    return listed


