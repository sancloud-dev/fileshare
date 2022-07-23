from flask import Flask, render_template, request
import config as keys
import boto3 
from werkzeug.utils import secure_filename

app = Flask(__name__)


dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN)

s3 = boto3.client('s3',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN
                      )
# s3 = boto3.client('s3')
BUCKET_NAME=keys.BUCKET_NAME

from boto3.dynamodb.conditions import Key, Attr

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['post'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        table = dynamodb.Table('users')
        
        table.put_item(
                Item={
        'name': name,
        'email': email,
        'password': password
            }
        )
        msg = "Registration Complete. Please Login to your account !"
    
        return render_template('login.html',msg = msg)
    return render_template('index.html')

@app.route('/login')
def login():    
    return render_template('login.html')


@app.route('/check',methods = ['post'])
def check():
    if request.method=='POST':
        
        email = request.form['email']
        password = request.form['password']
        
        table = dynamodb.Table('users')
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        name = items[0]['name']
        print(items[0]['password'])
        if password == items[0]['password']:            
            return render_template("home.html",name = name)
    return render_template("login.html")

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
                filename = secure_filename(file.filename)
                file.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )                        
        email_ist = [request.form['recipent1'], request.form['recipent2'], request.form['recipent3'], request.form['recipent4'], request.form['recipent5']]
         
        for email in email_ist:
            if email != "":
                #verified_email = ses.verify_email_identity(EmailAddress=email)

                s3_link = s3.generate_presigned_url(
                    ClientMethod='get_object',
                    Params={
                        'Bucket': BUCKET_NAME,
                        'Key': filename
                    },
                    ExpiresIn=3600,
                    HttpMethod='GET'
                )
                session = boto3.Session(
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN
                )
                client = session.client('ses')
                response = client.send_email(
                    Destination={
                        'ToAddresses': [email]
                    },
                    Message={
                        'Body': {
                            'Html': {
                                'Charset': 'UTF-8',
                                'Data': f'Hi {email}, \n\n Greetings from the FileShare Website.\n\n' + '<a href="' + s3_link + '">Click here to download the file</a>'
                            }
                        },
                        'Subject': {
                            'Charset': 'UTF-8',
                            'Data': 'FileShare Website'
                        }
                    },
                    Source=keys.SENDER_EMAIL,
                    SourceArn = keys.SOURCE_ARN, 
                )
    
    #strip empty spaces from the list
    email_ist = [email for email in email_ist if email != ""]
    msg= f"File {filename} has been shared with " + str(email_ist)
    # delete object in  s3  after sharing
    s3.delete_object(
        Bucket = BUCKET_NAME,
        Key = filename
    ) 
    return render_template("home.html",msg =msg) 
        
if __name__ == "__main__":
    
    app.run(debug=True)

