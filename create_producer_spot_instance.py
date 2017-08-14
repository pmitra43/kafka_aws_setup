import boto3
import base64

brokerIP=input("Please enter brokerIP:")
client = boto3.client('ec2')
file = open('producerUserData.sh', 'r')
userData=file.read().replace("$BROKER_IP",brokerIP)

encodedUserData=base64.b64encode(userData.encode())
response = client.request_spot_instances(
    InstanceCount=1,
    LaunchSpecification={
        'SecurityGroupIds': [
            'sg-e6d7188e',
        ],
        'EbsOptimized': False,
        'ImageId': 'ami-c73f44a8',
        'InstanceType': 'c4.xlarge',

        'Placement': {
            'AvailabilityZone': 'ap-south-1b',
            'Tenancy': 'default'
        },
        'SubnetId': 'subnet-d010849d',
        'UserData': str(encodedUserData.decode('utf-8'))
    },
    SpotPrice='0.06'
)

print(response)
