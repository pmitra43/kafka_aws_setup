import boto3

ec2=boto3.resource('ec2')
brokerIP=input("Please enter brokerIP:")

file=open("consumer_user_data.sh","r")
userData=file.read().replace("$BROKER_IP",brokerIP)

instance = ec2.create_instances(
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'DeleteOnTermination': True,
                'VolumeSize': 16,
                'VolumeType': 'gp2'
            }
        }
    ],
    ImageId='ami-09146e66',
    InstanceType='t2.micro',
    KeyName='New_MS_POC',
    MaxCount=1,
    MinCount=1,
    Monitoring={
        'Enabled': False
    },
    Placement={
        'AvailabilityZone': 'ap-south-1b',
        'Tenancy': 'default'
    },
    SecurityGroupIds=[
        'sg-e6d7188e',
    ],
    SubnetId='subnet-d010849d',
    UserData=userData,
    InstanceInitiatedShutdownBehavior='stop',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'test_consumer'
                },
            ]
        },
    ]
)

print(instance)
