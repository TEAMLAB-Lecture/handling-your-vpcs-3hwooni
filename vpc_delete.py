import boto3
from botocore.exceptions import ClientError
import datetime


client = boto3.client('ec2')

result = client.describe_security_groups()
groupid_list = []
try:
    for value in result["SecurityGroups"]:
        groupid_list.append(value['GroupId'])
        if value["GroupName"] == "launch-wizard-2":
            pass
        elif value["GroupName"] == "default":
            pass
        else:
            response = client.delete_security_group(GroupId=value["GroupId"])
            print('Security Group Deleted')
            time_log = datetime.datetime.now()
            id_log = value["GroupId"]
            with open('system_log.csv','a') as f:
                f.write("%s,%s,Deleted\n" % (id_log,time_log))
                f.close
    print(groupid_list)

except ClientError as e:
    with open('system_log.csv','a') as af:
         af.write("%s,Delete error\n" % (datetime.datetime.now()))
         af.close
