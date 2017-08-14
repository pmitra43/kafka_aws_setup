import boto3
import base64

brokerIP=input("Please enter brokerIP:")
instanceType=input("Please enter instance type:")
spotPrice=input("Please enter spot price:")
numberOfProducers=input("PLease enter number of producers you want to run on this machine:")
client = boto3.client('ec2')
file = open('producer_user_data.sh', 'r')
userData=file.read().replace("$BROKER_IP",brokerIP)
userData=userData.replace("$NUMBER_OF_PRODUCERS",numberOfProducers)

encodedUserData=base64.b64encode(userData.encode())
response = client.request_spot_instances(
    InstanceCount=1,
    LaunchSpecification={
        'SecurityGroupIds': [
            'sg-e6d7188e',
        ],
        'EbsOptimized': False,
        'ImageId': 'ami-c73f44a8',
        'InstanceType': instanceType,

        'Placement': {
            'AvailabilityZone': 'ap-south-1b',
            'Tenancy': 'default'
        },
        'SubnetId': 'subnet-d010849d',
        'UserData': str(encodedUserData.decode('utf-8'))
    },
    SpotPrice=spotPrice
)
