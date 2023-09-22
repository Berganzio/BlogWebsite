from flask import Flask, render_template, request
import requests
from email.message import EmailMessage
import ssl
import smtplib

app = Flask(__name__)

response = requests.get('https://api.npoint.io/0e42a5744418e4b28797').json()


@app.route('/')
def home():
    return render_template('index.html', all_posts=response)


@app.route('/about')
def get_about():
    return render_template('about.html')


@app.route('/contact')
def get_contact():
    return render_template('contact.html', name='Contact Me')


@app.route('/post')
def get_post():
    return render_template('post.html')


@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for post in response:
        if post['id'] == index:
            requested_post = post
    return render_template('post.html', post=requested_post)


@app.route("/contact", methods=["POST"])
def receive_data():
    data = request.form
    print(data["name"])
    print(data["email"])
    print(data["phone"])
    print(data["message"])
    email_sender = 'ISS.notifier.andrea@gmail.com'
    sender_psw = 'jgbmoatatlpdrmpq'
    email_receiver = 'andreamusic.bergantin@gmail.com'

    subject = 'Contact form'

    body = f"""name: {data["name"]}\nemail: {data["email"]}\nphone number: {data["phone"]}\nmessage: {data["message"]}"""

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, sender_psw)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    return render_template('contact.html', name='Succesfully sent your message')


while __name__ == '__main__':
    app.run(debug=True)
