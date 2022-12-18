import boto3
import json
import time

from botocore.exceptions import ClientError

from src.core import settings


# QuickSight Docs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html

# This provides a sort of QuickSight utilities

def get_quicksight_client():
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        return boto3.client(
            'quicksight',
            region_name=settings.AWS_DEFAULT_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
    return boto3.client('quicksight', region_name=settings.AWS_DEFAULT_REGION)


class QuickSightDashboardProvider():
    def __init__(self, client=None):
        self._client = client or get_quicksight_client()

    def get_dashboard_list(self):
        response = self._client.list_dashboards(AwsAccountId=settings.AWS_ACCOUNT_ID)
        # Response example:
        # {
        #   "ResponseMetadata": {
        #     "RequestId": "080b26c0-1297-4451-bdb5-5a5ee5b5eb9e",
        #     "HTTPStatusCode": 200,
        #     "HTTPHeaders": {
        #       "date": "Thu, 15 Dec 2022 17:29:14 GMT",
        #       "content-type": "application/json",
        #       "content-length": "398",
        #       "connection": "keep-alive",
        #       "x-amzn-requestid": "080b26c0-1297-4451-bdb5-5a5ee5b5eb9e"
        #     },
        #     "RetryAttempts": 0
        #   },
        #   "Status": 200,
        #   "DashboardSummaryList": [
        #     {
        #       "Arn": "arn:aws:quicksight:us-east-1:847766398334:dashboard/682e87f6-5039-4d80-8a93-9ba105a3c2e9",
        #       "DashboardId": "682e87f6-5039-4d80-8a93-9ba105a3c2e9",
        #       "Name": "OfficeCorp Sales",
        #       "CreatedTime": "2022-12-15T14:28:52.500000-03:00",
        #       "LastUpdatedTime": "2022-12-15T14:28:52.494000-03:00",
        #       "PublishedVersionNumber": 1,
        #       "LastPublishedTime": "2022-12-15T14:28:52.500000-03:00"
        #     }
        #   ],
        #   "RequestId": "080b26c0-1297-4451-bdb5-5a5ee5b5eb9e"
        # }
        return response['DashboardSummaryList']


class QuickSightAnalysisProvider:
    def __init__(self, client=None):
        self._client = client or get_quicksight_client()

    def get_analysis_list(self):
        response = self._client.list_analyses(AwsAccountId=settings.AWS_ACCOUNT_ID)
        # Response example:
        # {
        #   "ResponseMetadata": {
        #     "RequestId": "dcf0179f-aecc-4143-a55c-ef51e0864764",
        #     "HTTPStatusCode": 200,
        #     "HTTPHeaders": {
        #       "date": "Thu, 15 Dec 2022 17:02:28 GMT",
        #       "content-type": "application/json",
        #       "content-length": "2077",
        #       "connection": "keep-alive",
        #       "x-amzn-requestid": "dcf0179f-aecc-4143-a55c-ef51e0864764"
        #     },
        #     "RetryAttempts": 0
        #   },
        #   "Status": 200,
        #   "AnalysisSummaryList": [
        #     {
        #       "Arn": "arn:aws:quicksight:us-east-1:847766398334:analysis/1d1a81b5-8c79-4121-9d04-7ee3d8582841",
        #       "AnalysisId": "1d1a81b5-8c79-4121-9d04-7ee3d8582841",
        #       "Name": "OfficeCorp Sales analysis",
        #       "Status": "CREATION_SUCCESSFUL",
        #       "CreatedTime": "2022-12-13T23:07:52.126000-03:00",
        #       "LastUpdatedTime": "2022-12-13T23:09:31.879000-03:00"
        #     }
        #   ],
        #   "RequestId": "dcf0179f-aecc-4143-a55c-ef51e0864764"
        # }
        return response['AnalysisSummaryList']


# Example of Generating the URL with the authentication code attached for embedding in an iframe
# From https://docs.aws.amazon.com/quicksight/latest/user/embedded-analytics-dashboards-with-anonymous-users-step-2.html

# import json
# import boto3
# from botocore.exceptions import ClientError
# import time

# # Create QuickSight and STS clients
# quicksightClient = boto3.client('quicksight',region_name='us-east-1')
# sts = boto3.client('sts')

# # Function to generate embedded URL for anonymous user
# # accountId: YOUR AWS ACCOUNT ID
# # quicksightNamespace: VALID NAMESPACE WHERE YOU WANT TO DO NOAUTH EMBEDDING
# # authorizedResourceArns: DASHBOARD ARN LIST TO EMBED
# # allowedDomains: RUNTIME ALLOWED DOMAINS FOR EMBEDDING
# # experienceConfiguration: DASHBOARD ID TO WHICH THE CONSTRUCTED URL POINTS
# # sessionTags: SESSION TAGS USED FOR ROW-LEVEL SECURITY
# def generateEmbedUrlForAnonymousUser(accountId, quicksightNamespace, authorizedResourceArns, allowedDomains, experienceConfiguration, sessionTags):
#     try:
#         response = quicksightClient.generate_embed_url_for_anonymous_user(
#             "AwsAccountId" = accountId,
#             "Namespace" = quicksightNamespace,
#             "AuthorizedResourceArns" = authorizedResourceArns,
#             "AllowedDomains" = allowedDomains,
#             "ExperienceConfiguration" = experienceConfiguration,
#             "SessionTags" = sessionTags,
#             "SessionLifetimeInMinutes" = 600
#         )
            
#         return {
#             'statusCode': 200,
#             'headers': {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type"},
#             'body': json.dumps(response),
#             'isBase64Encoded':  bool('false')
#         }
#     except ClientError as e:
#         print(e)
#         return "Error generating embeddedURL: " + str(e)

class QuickSightEmbeddingProvider:
    def __init__(self, client=None):
        self._client = client or get_quicksight_client()
    
    def get_embedding_url(dashboard_arn, session_tags=None):
        response = self._client.generate_embed_url_for_anonymous_user(
            AwsAccountId=settings.AWS_ACCOUNT_ID,
            Namespace=settings.AWS_QUICKSIGHT_NAMESPACE,
            AuthorizedResourceArns=[dashboard_arn],
            AllowedDomains=settings.ALLOWED_DOMAINS,
            ExperienceConfiguration={
                'DashboardId': dashboard_arn,
            },
            SessionTags=session_tags,
            SessionLifetimeInMinutes=600
        )
        # Response example:
        # {
        #   "ResponseMetadata": {
        #     "RequestId": "b2d8a7b9-0f6c-4a2b-8b8f-0e5a7c5c5e1e",
        #     "HTTPStatusCode": 200,
        #     "HTTPHeaders": {
        #       "date": "Thu, 15 Dec 2022 17:02:28 GMT",
        #       "content-type": "application/json",
        #       "content-length": "2077",
        #       "connection": "keep-alive",
        #       "x-amzn-requestid": "dcf0179f-aecc-4143-a55c-ef51e0864764"
        #     },
        #     "RetryAttempts": 0
        #   },
        #   "EmbedUrl": "https://quicksight.aws.amazon.com/sn/dashboards/682e87f6-5039-4d80-8a93-9ba105a3c2e9?isauthcode=true&identityprovider=quicksight&code=eyJraWQiOiJkYXNoYm9hcmQtdG9rZW4iLCJhbGciOiJS
        #   "Status": 200,
        #   "RequestId": "dcf0179f-aecc-4143-a55c-ef51e0864764"
        # }
        return response['EmbedUrl']
        
        

