import boto3
import time
import datetime
from botocore.exceptions import ClientError



ec2 = boto3.client('ec2')

response = ec2.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

for i in range(10):
    try:
            response = ec2.create_security_group(GroupName=str(i)+'HelloChaewoon',
                                                 Description='Made by boto3',
                                                 VpcId='vpc-9a5b7cfd')

            security_group_id = response['GroupId']
            print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

            data = ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                     'FromPort': 80,
                     'ToPort': 80,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                     'FromPort': 22,
                     'ToPort': 22,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ])
            print('Ingress Successfully Set %s' % data)

            with open("system_log.csv","a") as f:
                time_log = data["ResponseMetadata"]['HTTPHeaders']['date']
                f.write("%s,%s,Created\n" % (security_group_id,time_log))
                f.close

            # timeout = time.time() + 5
            # while True:
            #     if time.time() > timeout:
            #         break
    except ClientError as e:
        with open("system_log.csv", "a") as af:

            error_time_log = datetime.datetime.now()

            af.write("%s,Create Error\n" % (error_time_log))
            af.close
        print(e)
