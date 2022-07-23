import boto3
# Get the service resource.
import config as keys


dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN)
 
# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='users',
    KeySchema=[
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        }
         
    ],
    AttributeDefinitions=[
             {
            'AttributeName': 'email',
            'AttributeType': 'S'
        } 
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='users')

# Print out some data about the table.
print(table.item_count)

#artifact-bucket-fileshare
s3 = boto3.client('s3')
s3.create_bucket(ACL = 'public-read-write', Bucket=keys.BUCKET_NAME)

#Verfiy source email in  SES
 
ses = boto3.client('ses')
response = ses.verify_email_identity(EmailAddress=keys.SENDER_EMAIL)
print(response)



 