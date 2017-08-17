import boto3
import base64

client=boto3.client('ec2')
brokerIP=input("Please enter brokerIP:")

file=open("consumer_user_data.sh","r")
userData=file.read().replace("$BROKER_IP",brokerIP)

encodedUserData=base64.b64encode(userData.encode())

response = client.request_spot_instances(
    InstanceCount=1,
    LaunchSpecification={
        'SecurityGroupIds': [
            'sg-e6d7188e'
        ],
        'KeyName': 'New_MS_POC',
        'EbsOptimized': False,
        'ImageId': 'ami-09146e66',
        'InstanceType': 'r4.xlarge',
        'Placement': {
            'AvailabilityZone': 'ap-south-1b',
            'Tenancy': 'default',
        },
        'SubnetId': 'subnet-d010849d',
        'UserData': encodedUserData.decode('utf-8'),
    },
    SpotPrice='0.06'
)

print(response)
