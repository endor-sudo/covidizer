import requests, json, os, platform, threading, getpass
import matplotlib.pyplot as plt
import email, smtplib, ssl, time, datetime, os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def console():
    while True:
        global send_hour, send_minute, sep
        command = input()
        if command=='update':
            while True:
                send_time=input('What is the time(hh:mm) to send the email?')
                try:
                    send_hour=int(send_time[0:2])
                    send_minute=int(send_time[-2:])
                    sep=send_time[2]
                except Exception:
                    print('NOT A VALID TIME!')
                else:
                    if len(send_time)<6 and send_hour<25 and send_minute<61 and sep==':':
                        print(f'alarm set to {send_hour}:{send_minute}')
                        break
                    else:
                        print('NOT A VALID TIME!')
                        send_hour=0
                        send_minute=0
                        sep=0

counter = getpass.getpass("Type your email counter and press enter:")
if platform.system()=='Darwin':
    sysclear='clear'
elif platform.system()=='Windows':
    sysclear='cls'
else:
    print('os.error')
clear=lambda:os.system(sysclear)
clear()
url='https://coronavirus-tracker-api.herokuapp.com/all'
send_hour=0
send_minute=0
sep=0
consoleObj=threading.Thread(target=console)
consoleObj.start()

while True:
    time_tag=datetime.datetime.now()
    if time_tag.hour==send_hour and time_tag.minute==send_minute:
        json_=requests.get(url)
        dict_=json.loads(json_.text)
        days=0
        country_id=0

        #get country's id
        for location in dict_['confirmed']['locations']:
            if location['country']=='Portugal':
                break
            country_id+=1

        updated=dict_['confirmed']['last_updated']
        country=dict_['confirmed']['locations'][country_id]['country']
        confirmed_cases=dict_['confirmed']['locations'][country_id]['latest']
        deaths=dict_['deaths']['locations'][country_id]['latest']
        recovered=dict_['recovered']['locations'][country_id]['latest']

        history=dict_['confirmed']['locations'][country_id]['history']
        x_values=[]
        y_values=[]

        for case_numbers in history.values():
            if int(case_numbers)>0:
                y_values.append(int(case_numbers))
                days+=1

        s_y_values=sorted(y_values)
        x_values=range(1,days+1)

        plt.plot(x_values,s_y_values,linewidth=5)

        # Set chart title and label axes.
        plt.title(f"{country} desde 02/03-C{confirmed_cases};M{deaths};R{recovered}", fontsize=24)
        plt.xlabel("Dias", fontsize=14)
        plt.ylabel("Casos", fontsize=14)

        plt.savefig(f'sars{updated[:10]}.png', bbox_inches='tight')

        subject = f"Casos de CoViD-19 em {country} desde 02/03"
        body = "This is an email with attachment sent from Python"
        sender_email = "vender123@sapo.pt"
        receiver_email = "vender123@sapo.pt"

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = f'sars{updated[:10]}.png'  # In same directory as script

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.sapo.pt", 465, context=context) as server:
            server.login(sender_email, counter)
            server.sendmail(sender_email, receiver_email, text)
            
        print(f'Email enviado às {time_tag.hour}:{time_tag.minute}:{time_tag.second} de {time_tag.day}/{time_tag.month}/{time_tag.year}')
        time.sleep(61)