import boto3
import base64

client = boto3.client('ec2')
zookeeperIP=input("Please enter zookeeperIP: ")
instanceType=input("Enter instance type: ")
spotPrice=input("Please enter spot price: ")

file=open("broker_user_data.sh","r")
userData=file.read().replace("$ZOOKEEPER_IP",zookeeperIP)

encodedUserData=base64.b64encode(userData.encode())

response = client.request_spot_instances(
    InstanceCount=1,
    LaunchSpecification={
        'SecurityGroupIds': [
            'sg-633ff10b'
        ],
        'KeyName': 'New_MS_POC',
        'EbsOptimized': False,
        'ImageId': 'ami-3f88f350',
        'InstanceType': instanceType,
        'Placement': {
            'AvailabilityZone': 'ap-south-1b',
            'Tenancy': 'default',
        },
        'SubnetId': 'subnet-1e128653',
        'UserData': encodedUserData.decode('utf-8'),
    },
    SpotPrice=spotPrice
)

print(response)
