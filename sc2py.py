import matplotlib.pyplot as plt
import numpy as np
import getpass
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sarcscovdb import *

cases=[v for v in case_history.values()]

newCases=[]
pnc=0
for v in case_history.values():
    nc=v-pnc
    pnc=v
    newCases.append(nc)

newReco=[]
pnr=0
for v in reco_history.values():
    nr=v-pnr
    pnr=v
    newReco.append(nr)

newDeat=[]
pnd=0
for v in deat_history.values():
    nd=v-pnd
    pnd=v
    newDeat.append(nd)
deaths=[v for v in deat_history.values()]

recovered=[v for v in reco_history.values()]
deaths=[v for v in deat_history.values()]

height=15
width=height*1.5
plt.figure(figsize=(width,height))

#regressions
case_reg= np.poly1d(np.polyfit(cases,newCases, 10))
print(case_reg)
plt.plot(cases, case_reg(cases))

reco_reg= np.poly1d(np.polyfit(cases,newReco, 10))
print(reco_reg)
#plt.plot(cases, reco_reg(cases),c='green')

deat_reg= np.poly1d(np.polyfit(cases,newDeat, 10))
print(deat_reg)
plt.plot(cases, deat_reg(cases),c='red')
#legend
plt.scatter(cases,newCases, edgecolors='none',s=25,c='blue',label=f'cases (latest: {cases[-1]})')
#plt.scatter(cases,newReco, edgecolors='none',s=15,c='green',label=f'recovered (latest: {recovered[-1]})')
plt.scatter(cases,newDeat, edgecolors='none',s=15,c='red',label=f'deaths (latest: {deaths[-1]}; '
    f'{round(deaths[-1]/cases[-1]*100,2)}% of blue; {round(deaths[-1]/recovered[-1]*100,2)}% of green)')
#Show legend
plt.legend()
# Set chart title and label axes. 
plt.title(f"CoVid-19 in Portugal", fontsize=24) 
plt.xlabel("Total cases", fontsize=14) 
plt.ylabel("New per day", fontsize=14)
# Set size of tick labels.
plt.tick_params(axis='both', which='major', labelsize=10)

#log scale
plt.yscale('log')
lim=[]
lim.append(max(newCases))
lim.append(max(newReco))
lim.append(max(newDeat))

#percentage growth from y=mx+b
case_reg= np.poly1d(np.polyfit(cases,newCases, 1))
exp=[case_reg(v) for v in case_history.values() ]
plt.plot(cases,exp,label=f'{case_reg}')
plt.legend(loc="upper left")

plt.ylim(bottom=0.9)

#Save file
plt.savefig(f'sarsDaylog{len(case_history)}.png', bbox_inches='tight')

plt.show()
"""
subject = "Casos de CoViD-19 em Portugal desde 02/03"
body = "This is an email with attachment sent from Python"
sender_email = "vender123@sapo.pt"
receiver_email = "vender123@sapo.pt"
counter = getpass.getpass("Type your email counter and press enter:")

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))

filename = f'sarsDay{len(case_history)}.png'  # In same directory as script

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
"""