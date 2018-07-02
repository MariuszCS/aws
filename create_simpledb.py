import boto3

simpledb = boto3.client('sdb')
simpledb.create_domain(DomainName='ProjectSimpleDB')
