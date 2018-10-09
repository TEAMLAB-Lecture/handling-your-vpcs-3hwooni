import boto3
import botocore

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
    
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        s3 = boto3.client('s3')
        filename = 'system_log.csv'
        s3.upload_file(filename, bucket_name, filename)
        print("File uploaded")
    else:
        raise
##버켓 안에 파일이 있으면 다운로드

# s3 = boto3.client('s3')
#
# bucket_name = 's3buckethomework'
# filename = 'system_log.csv'
# s3.upload_file(filename, bucket_name, filename)
# print("File uploaded")
