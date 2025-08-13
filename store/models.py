import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.db import models

# Configure DynamoDB client to use local endpoint
dynamodb = boto3.resource(
    'dynamodb',
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    endpoint_url=settings.DYNAMODB_ENDPOINT_URL
)

def get_or_create_table():
    try:
        table = dynamodb.create_table(
            TableName='Products',
            KeySchema=[
                {
                    'AttributeName': 'product_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'product_id',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()
        return table
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            return dynamodb.Table('Products')
        raise

products_table = get_or_create_table()




class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name