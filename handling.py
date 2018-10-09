import boto3
import time
import datetime
from botocore.exceptions import ClientError
import botocore




def create_vpc():
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

                timeout = time.time() + 5
                while True:
                    if time.time() > timeout:
                        break
        except ClientError as e:
            with open("system_log.csv", "a") as af:

                error_time_log = datetime.datetime.now()

                af.write("%s,Create Error\n" % (error_time_log))
                af.close
            print(e)

def delete_vpc():
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


def create_s3():
    s3 = boto3.resource('s3')

    s3_list = []

    for bucket in s3.buckets.all():
        s3_list.append(bucket.name)
    ### 버켓 이름들 리스트에 저장

    s3 = boto3.client('s3', region_name="ap-southeast-1")
    if "s3buckethomework" not in s3_list:
        response = s3.create_bucket(
            Bucket='s3buckethomework',
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-southeast-1'
                }
            )
        print("Bucket created")
    else:
        print("Bucket already exist")
    ### 버켓이 존재하지 않으면 생성


    bucket_name = 's3buckethomework'
    Key = 'system_log.csv'

    s3 = boto3.resource('s3')

    try:
        s3.Bucket(bucket_name).download_file(Key, 'downloadfile.csv')
        s3_file = open("downloadfile.csv")
        new_file = open("system_log.csv")

        s3_file_lines = s3_file.readlines()
        new_file_lines = new_file.readlines()

        s3_file_lines = [line.strip() for line in s3_file_lines]
        new_file_lines = [line.strip() for line in new_file_lines]

        final_lines = []

        for line in s3_file_lines:
            if line not in final_lines:
                final_lines.append(line)

        for line in new_file_lines:
            if line not in final_lines:
                final_lines.append(line)

        lines = "\n".join(final_lines)

        file = open("system_log.csv","w")
        file.write(lines+"\n")
        file.close()

        s3 = boto3.client('s3')
        filename = 'system_log.csv'
        s3.upload_file(filename, bucket_name, filename)
        print("File Updated")
        ### 버켓안에 파일이 있으면 다운로드 후 업데이트
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            s3 = boto3.client('s3')
            filename = 'system_log.csv'
            s3.upload_file(filename, bucket_name, filename)
            print("File uploaded")
        else:
            raise
        ### 버켓안에 파일이 없을경우 업로드



if __name__ == "__main__":
    create_vpc()
    delete_vpc()
    create_s3()
