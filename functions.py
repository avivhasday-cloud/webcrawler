import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_html_of_job(job, base_url):
    details = job['details']
    requirements = job['requirements']
    link = base_url + job['link']
    return """
            <div>
                <div>
                    <h3>Details</h3>
                    <p>{0}</p>
                </div><br/>
                <div>
                    <h3>Requirements</h3>
                    <p>{1}</p>
                </div><br/><div>
                    <h3>Link:</h3>
                    <p>{2}</p>
                </div>
            </div><br/>
            <hr/>    
    """.format(details, requirements, link)


def get_categories_data(base_url):
    url = "{0}/api/cache/categories".format(base_url)
    res = requests.get(url, stream=True)
    data = res.json()["ResultList"]
    category_list = []
    for i in range(len(data)):
        for object in data[i]["Areas"]:
            category_list.append(object)

    return category_list

def get_category_path(word, base_url):
    data = get_categories_data(base_url)
    for obj in data:
        if word in obj['NameInHebrew'].lower():
            path = obj['Link']
            return base_url + path

def send_mail(html, user):
    mail_content = html
    #The mail addresses and password
    sender_address = 'pythondevelopment400@gmail.com'
    sender_pass = 'Aa123456!'
    receiver_address = user
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Job Offer'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'html'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')



if __name__ == "__main__":
    data = get_categories_data('https://www.drushim.co.il/')
    for line in data:
        print(line)






