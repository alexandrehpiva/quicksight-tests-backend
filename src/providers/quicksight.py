import boto3
import json
import time
import re

from botocore.exceptions import ClientError
from fastapi import HTTPException
from starlette import status

from src.core import settings


# This file provides a sort of QuickSight utilities
# QuickSight Docs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html


# Utilities

def get_quicksight_client():
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        return boto3.client(
            'quicksight',
            region_name=settings.AWS_DEFAULT_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
    return boto3.client('quicksight', region_name=settings.AWS_DEFAULT_REGION)


# Exceptions

class QuickSightExceptions:
    class PricingPlanException(Exception):
        def __init__(self, e):
            message = 'The current pricing plan does not support generating an embedding URL for anonymous users'
            print(f'{message}: {e}')
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)
    
    class EmbeddingException(Exception):
        def __init__(self, e):
            message = 'There was an error generating the embedding URL'
            print(f'{message}: {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)

    class UserException(Exception):
        def __init__(self, e):
            message = 'There was an error obtaining the user information'
            print(f'{message}: {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)


# Providers

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

    def _get_dashboard_by_key_item_name(self, key_item_name, key_item_value):
        dashboard = next((dashboard for dashboard in self.get_dashboard_list() if key_item_value in dashboard.get(key_item_name, '')), None)
        if dashboard is None:
            raise KeyError(f'Dashboard with {key_item_name} "{key_item_value}" not found')
        return dashboard
    
    def get_dashboard_by_name(self, name):
        return self._get_dashboard_by_key_item_name('Name', name)
    
    def get_dashboard_by_id(self, id):
        return self._get_dashboard_by_key_item_name('DashboardId', id)


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


class QuickSightDataSourceProvider:
    def __init__(self, client=None):
        self._client = client or get_quicksight_client()

    def get_data_source_list(self):
        response = self._client.list_data_sources(AwsAccountId=settings.AWS_ACCOUNT_ID)
        # Response example:
        # {
        #   "ResponseMetadata": {
        #     "RequestId": "f6c8f6d7-6c5b-4d7c-bd8f-7c6b9c9b3d3c",
        #     "HTTPStatusCode": 200,
        #     "HTTPHeaders": {
        #       "date": "Thu, 15 Dec 2022 17:00:27 GMT",
        #       "content-type": "application/json",
        #       "content-length": "319",
        #       "connection": "keep-alive",
        #       "x-amzn-requestid": "f6c8f6d7-6c5b-4d7c-bd8f-7c6b9c9b3d3c"
        #     },
        #     "RetryAttempts": 0
        #   },
        #   "Status": 200,
        #   "DataSourceSummaryList": [
        #     {
        #       "Arn": "arn:aws:quicksight:us-east-1:847766398334:datasource/1d1a81b5-8c79-4121-9d04-7ee3d8582841",
        #       "DataSourceId": "1d1a81b5-8c79-4121-9d04-7ee3d8582841",
        #       "Name": "OfficeCorp Sales data source",
        #       "Type": "AURORA",
        #       "CreatedTime": "2022-12-13T23:07:52.126000-03:00",
        #       "LastUpdatedTime": "2022-12-13T23:09:31.879000-03:00"
        #     }
        #   ],
        #   "RequestId": "f6c8f6d7-6c5b-4d7c-bd8f-7c6b9c9b3d3c"
        # }
        return response['DataSourceSummaryList']


class QuickSightEmbeddingProvider:
    def __init__(self, client=None):
        self._client = client or get_quicksight_client()
    
    def get_dashboard_embedding_url_for_anonymous_user(self, dashboard_id, session_tags=None) -> str:
        """
        Get the embedding URL for a dashboard
        :param dashboard_id: The ID of the dashboard to embed
        :param session_tags: A list of tags to apply to the session
            Example:
            session_tags = [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        :return: The embedding URL
        """
        dashboard_arn = QuickSightDashboardProvider(self._client).get_dashboard_by_id(dashboard_id).get('Arn')
        # Docs: https://docs.aws.amazon.com/quicksight/latest/APIReference/API_GenerateEmbedUrlForAnonymousUser.html
        params = {
            'AwsAccountId': settings.AWS_ACCOUNT_ID,
            'Namespace': settings.AWS_QUICKSIGHT_NAMESPACE,
            'AuthorizedResourceArns': [dashboard_arn],
            'ExperienceConfiguration': {
                'Dashboard': {
                    'InitialDashboardId': dashboard_id
                }
            },
            'SessionLifetimeInMinutes': 30
        }
        if session_tags:
            params['SessionTags'] = session_tags
        if settings.AWS_QUICKSIGHT_ALLOWED_DOMAINS:
            params['AllowedDomains'] = settings.AWS_QUICKSIGHT_ALLOWED_DOMAINS.split(',')
        try:
            response = self._client.generate_embed_url_for_anonymous_user(**params)
            return response.get('EmbedUrl')
        except ClientError as e:
            if re.match(r'UnsupportedPricingPlanException', e.response.get('Error', {}).get('Code')):
                raise QuickSightExceptions.PricingPlanException(e) from e
            raise QuickSightExceptions.EmbeddingException(e) from e

    def get_dashboard_embedding_url_for_registered_user(self, dashboard_id, user_arn=None, user_name=None, session_tags=None) -> str:
        """
        Get the embedding URL for a dashboard
        :param dashboard_id: The ID of the dashboard to embed
        :param user_arn: The ARN of the user to embed
        :param session_tags: A list of tags to apply to the session
            Example:
            session_tags = [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        :return: The embedding URL
        """
        if not user_arn and not user_name:
            raise QuickSightExceptions.EmbeddingException('You must provide either a user ARN or a user name')
        elif user_arn and user_name:
            user_arn = QuickSightUserProvider(self._client).get_user_by_name(user_name).get('Arn')
        # dashboard = QuickSightDashboardProvider(self._client).get_dashboard_by_id(dashboard_id)
        # Docs: https://docs.aws.amazon.com/quicksight/latest/APIReference/API_GenerateEmbedUrlForRegisteredUser.html
        params = {
            'AwsAccountId': settings.AWS_ACCOUNT_ID,
            'ExperienceConfiguration': {
                'Dashboard': {
                    # 'InitialDashboardId': dashboard.get('DashboardId'),
                    'InitialDashboardId': dashboard_id,
                }
            },
            'SessionLifetimeInMinutes': 30,
            'UserArn': user_arn
        }
        if session_tags:
            params['SessionTags'] = session_tags
        if settings.AWS_QUICKSIGHT_ALLOWED_DOMAINS:
            params['AllowedDomains'] = settings.AWS_QUICKSIGHT_ALLOWED_DOMAINS.split(',')
        try:
            response = self._client.generate_embed_url_for_registered_user(**params)
            return response.get('EmbedUrl')
        except ClientError as e:
            if re.match(r'UnsupportedPricingPlanException', e.response.get('Error', {}).get('Code')):
                raise QuickSightExceptions.PricingPlanException(e) from e
            raise QuickSightExceptions.EmbeddingException(e) from e


class QuickSightUserProvider:
    def __init__(self, client=None):
        self._client = client or get_quicksight_client()
    
    def get_user_list(self) -> list:
        """
        List all users
        :return: A list of users
            example:
            [
                {
                    "Arn": "arn:aws:quicksight:us-east-1:847766398334:user/default/alexandrehpiva-dev",
                    "UserName": "alexandrehpiva-dev",
                    "Email": "alexandrehpiva@gmail.com",
                    "Role": "ADMIN",
                    "IdentityType": "IAM",
                    "Active": true,
                    "PrincipalId": "federated/iam/AIDA4KYWQUV7IQJSEQIKJ"
                }
            ]
        """
        # Docs: https://docs.aws.amazon.com/quicksight/latest/APIReference/API_ListUsers.html
        try:
            response = self._client.list_users(
                AwsAccountId=settings.AWS_ACCOUNT_ID,
                Namespace=settings.AWS_QUICKSIGHT_NAMESPACE
            )
            return response.get('UserList')
        except ClientError as e:
            if re.match(r'UnsupportedPricingPlanException', e.response.get('Error', {}).get('Code')):
                raise QuickSightExceptions.PricingPlanException(e) from e
            raise QuickSightExceptions.UserException(e) from e
    
    def get_user_by_arn(self, user_arn) -> dict:
        """
        Get a user by ARN
        :param user_arn: The ARN of the user
        :return: The user
        """
        # Docs: https://docs.aws.amazon.com/quicksight/latest/APIReference/API_DescribeUser.html
        try:
            response = self._client.describe_user(
                AwsAccountId=settings.AWS_ACCOUNT_ID,
                Namespace=settings.AWS_QUICKSIGHT_NAMESPACE,
                UserName=user_arn
            )
            return response.get('User')
        except ClientError as e:
            if re.match(r'UnsupportedPricingPlanException', e.response.get('Error', {}).get('Code')):
                raise QuickSightExceptions.PricingPlanException(e) from e
            raise QuickSightExceptions.UserException(e) from e
    
    def get_user_by_email(self, email) -> dict:
        """
        Get a user by email
        :param email: The email of the user
        :return: The user
        """
        # Docs: https://docs.aws.amazon.com/quicksight/latest/APIReference/API_DescribeUser.html
        try:
            response = self._client.describe_user(
                AwsAccountId=settings.AWS_ACCOUNT_ID,
                Namespace=settings.AWS_QUICKSIGHT_NAMESPACE,
                UserName=email
            )
            return response.get('User')
        except ClientError as e:
            if re.match(r'UnsupportedPricingPlanException', e.response.get('Error', {}).get('Code')):
                raise QuickSightExceptions.PricingPlanException(e) from e
            raise QuickSightExceptions.UserException(e) from e
    
    def get_user_by_name(self, name) -> dict:
        """
        Get a user by username
        :param username: The username of the user
        :return: The user
        """
        # Docs: https://docs.aws.amazon.com/quicksight/latest/APIReference/API_DescribeUser.html
        try:
            response = self._client.describe_user(
                AwsAccountId=settings.AWS_ACCOUNT_ID,
                Namespace=settings.AWS_QUICKSIGHT_NAMESPACE,
                UserName=name
            )
            return response.get('User')
        except ClientError as e:
            if re.match(r'UnsupportedPricingPlanException', e.response.get('Error', {}).get('Code')):
                raise QuickSightExceptions.PricingPlanException(e) from e
            raise QuickSightExceptions.UserException(e) from e
