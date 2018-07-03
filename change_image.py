import boto3
import skimage
import skimage.io
import skimage.transform
import os
import datetime

sqs = boto3.resource("sqs", region_name='us-west-2')
queue = sqs.get_queue_by_name(QueueName="ProjectQueue")
s3 = boto3.resource('s3')
simpledb = boto3.client("sdb")

while True:
    message_list = queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=30)
    for message in message_list:
        image_name = message.body
        image = s3.meta.client.download_file("mariuszproject", "images/{0}".format(image_name), "temp_{0}".format(image_name))
        image_to_transform = skimage.io.imread("temp_{0}".format(image_name))
        transformed_image = skimage.transform.rotate(image_to_transform, 180)
        skimage.io.imsave("transformed_{0}".format(image_name), transformed_image)
        s3.meta.client.upload_file("transformed_{0}".format(image_name), "mariuszproject", "transformed/{0}".format(image_name))
        simpledb.put_attributes(DomainName="ProjectSimpleDB", ItemName="TransformedImage",
        Attributes=[{"Name":"Name", "Value":"transformed_{0}".format(image_name), "Replace":True}, {"Name":"Time", "Value":str(datetime.datetime.now()), "Replace":True}])

        message.delete()
        os.remove("temp_{0}".format(image_name))
        os.remove("transformed_{0}".format(image_name))
