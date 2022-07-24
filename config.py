#!/usr/bin/python3
#Fetch aws  credintials from config.json
import json
# with open(file='.\config.json', mode='r') as config_file: 
#     config_file = config_file.read().replace('"', "'").replace('ÿþ','')

# config = json.loads( config_file )
config = {
    "Credentials": {
      "AccessKeyId": "ASIA4DH7H5SKT5ZJF6OT",
      "SecretAccessKey": "Y1TJTjzyLDfHzff7AqAmpXpp2pR8e7lT3pHbYrP3",
      "SessionToken": "FwoGZXIvYXdzEEEaDKGCPPzGfcrpU+hR7SKpAXWSrCgmqQOMBhlrEDRwzce2gpvd0GaO8S4+R7sm2tgUSc+oEG7J/HrM4Hrxw/ie60hdMU/RoPhaRl1bu67SMLX6tzOKyhJ/5rUFRaAyr/x/tHBdus2WD+0I8TLfXhK4dJrDpJIMvDpGYNnY4UMXPubtfDq/kpSP54CGWM9hUsfRfTP0XVenHdKytvJF2uN40Gs7nHVMY6yIErwVI7pQIDU3Yuaf/jK7qu8o5aXwlgYyLV5f3xnO8cRqnFf2c+ZRn2DrqnMSOtwgpVtXCUtdirTJ77hqPdhaE35Cm+Vrug==",
      "Expiration": "2022-07-23T16:25:25Z"
    },
    "AssumedRoleUser": {
      "AssumedRoleId": "AROA4DH7H5SKR22YHE7YI:power",
      "Arn": "arn:aws:sts::831611464853:assumed-role/power-user/power"
    }
}
 
config = config['Credentials']

ACCESS_KEY_ID= config['AccessKeyId']
ACCESS_SECRET_KEY= config['SecretAccessKey']
AWS_SESSION_TOKEN= config['SessionToken']
BUCKET_NAME='fileshare-artifacts'
SENDER_EMAIL='santhoshreddyparapati@gmail.com'
SOURCE_ARN='arn:aws:ses:us-east-1:831611464853:identity/santhoshreddyparapati@gmail.com'