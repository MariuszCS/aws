import boto3

simpledb = boto3.client('sdb')


print(simpledb.list_domains())
print("~~~~~~~~~~~~~~")
print(simpledb.get_attributes(DomainName="ProjectSimpleDB", ItemName="Image"))
