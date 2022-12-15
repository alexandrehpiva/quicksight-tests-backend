import boto3

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

# list_dashboards(**kwargs)
#
#     Lists dashboards in an Amazon Web Services account.
#
#     See also: AWS API Documentation
#
#     Request Syntax
#
#     response = client.list_dashboards(
#         AwsAccountId='string',
#         NextToken='string',
#         MaxResults=123
#     )
#
#     Parameters
#
#             AwsAccountId (string) --
#
#             [REQUIRED]
#
#             The ID of the Amazon Web Services account that contains the dashboards that you're listing.
#             NextToken (string) -- The token for the next set of results, or null if there are no more results.
#             MaxResults (integer) -- The maximum number of results to be returned per request.
#
#     Return type
#
#         dict
#     Returns
#
#         Response Syntax
#
#         {
#             'DashboardSummaryList': [
#                 {
#                     'Arn': 'string',
#                     'DashboardId': 'string',
#                     'Name': 'string',
#                     'CreatedTime': datetime(2015, 1, 1),
#                     'LastUpdatedTime': datetime(2015, 1, 1),
#                     'PublishedVersionNumber': 123,
#                     'LastPublishedTime': datetime(2015, 1, 1)
#                 },
#             ],
#             'NextToken': 'string',
#             'Status': 123,
#             'RequestId': 'string'
#         }
#
#         Response Structure
#
#             (dict) --
#
#                 DashboardSummaryList (list) --
#
#                 A structure that contains all of the dashboards in your Amazon Web Services account. This structure provides basic information about the dashboards.
#
#                     (dict) --
#
#                     Dashboard summary.
#
#                         Arn (string) --
#
#                         The Amazon Resource Name (ARN) of the resource.
#
#                         DashboardId (string) --
#
#                         Dashboard ID.
#
#                         Name (string) --
#
#                         A display name for the dashboard.
#
#                         CreatedTime (datetime) --
#
#                         The time that this dashboard was created.
#
#                         LastUpdatedTime (datetime) --
#
#                         The last time that this dashboard was updated.
#
#                         PublishedVersionNumber (integer) --
#
#                         Published version number.
#
#                         LastPublishedTime (datetime) --
#
#                         The last time that this dashboard was published.
#
#                 NextToken (string) --
#
#                 The token for the next set of results, or null if there are no more results.
#
#                 Status (integer) --
#
#                 The HTTP status of the request.
#
#                 RequestId (string) --
#
#                 The Amazon Web Services request ID for this operation.
#
#     Exceptions
#
#         QuickSight.Client.exceptions.ThrottlingException
#         QuickSight.Client.exceptions.InvalidNextTokenException
#         QuickSight.Client.exceptions.UnsupportedUserEditionException
#         QuickSight.Client.exceptions.InternalFailureException

class QuickSightDashboardProvider:
    def __init__(self):
        self._client = get_quicksight_client()

    def get_dashboard_list(self):
        dashboards = self._client.list_dashboards(AwsAccountId=settings.AWS_ACCOUNT_ID)
        # Response example:
        # {
        #   "ResponseMetadata": {
        #     "RequestId": "a1f364ae-26c6-42e4-8a56-fa83299390e8",
        #     "HTTPStatusCode": 200,
        #     "HTTPHeaders": {
        #       "date": "Thu, 15 Dec 2022 16:53:43 GMT",
        #       "content-type": "application/json",
        #       "content-length": "95",
        #       "connection": "keep-alive",
        #       "x-amzn-requestid": "a1f364ae-26c6-42e4-8a56-fa83299390e8"
        #     },
        #     "RetryAttempts": 0
        #   },
        #   "Status": 200,
        #   "DashboardSummaryList": [
        #     {
        #       "Arn": "arn:aws:quicksight:us-east-1:123456789012:dashboard/12345678-1234-1234-1234-123456789012",
        #       "DashboardId": "12345678-1234-1234-1234-123456789012",
        #       "Name": "My Dashboard",
        #       "CreatedTime": "2021-12-15T16:53:43.000Z",
        #       "LastUpdatedTime": "2021-12-15T16:53:43.000Z",
        #       "PublishedVersionNumber": 1,
        #       "LastPublishedTime": "2021-12-15T16:53:43.000Z"
        #     }
        #   "RequestId": "a1f364ae-26c6-42e4-8a56-fa83299390e8"
        # }
        return dashboards

    def get_dashboard_url(self, dashboard_id):
        dashboard_url = self._client.get_dashboard_embed_url(
            AwsAccountId=settings.AWS_ACCOUNT_ID,
            DashboardId=dashboard_id,
            IdentityType="IAM",
            SessionLifetimeInMinutes=1000,
            UndoRedoDisabled=True,
            ResetDisabled=True,
        )
        # Response example:
        # {
        #   "ResponseMetadata": {
        #     "RequestId": "a1f364ae-26c6-42e4-8a56-fa83299390e8",
        #     "HTTPStatusCode": 200,
        #     "HTTPHeaders": {
        #       "date": "Thu, 15 Dec 2022 16:53:43 GMT",
        #       "content-type": "application/json",
        #       "content-length": "95",
        #       "connection": "keep-alive",
        #       "x-amzn-requestid": "a1f364ae-26c6-42e4-8a56-fa83299390e8"
        #     },
        #     "RetryAttempts": 0
        #   },
        #   "EmbedUrl": "https://quicksight.aws.amazon.com/sn/dashboards/12345678-1234-1234-1234-123456789012?isauthcode=true&identitytype=IAM&sessionlifetime=1000&undo_redo_disabled=true&reset_disabled=true&...",
        #   "Status": 200,
        #   "RequestId": "a1f364ae-26c6-42e4-8a56-fa83299390e8"
        # }
        return dashboard_url

# list_analyses(**kwargs)
#
#     Lists Amazon QuickSight analyses that exist in the specified Amazon Web Services account.
#
#     See also: AWS API Documentation
#
#     Request Syntax
#
#     response = client.list_analyses(
#         AwsAccountId='string',
#         NextToken='string',
#         MaxResults=123
#     )
#
#     Parameters
#
#             AwsAccountId (string) --
#
#             [REQUIRED]
#
#             The ID of the Amazon Web Services account that contains the analyses.
#             NextToken (string) -- A pagination token that can be used in a subsequent request.
#             MaxResults (integer) -- The maximum number of results to return.
#
#     Return type
#
#         dict
#     Returns
#
#         Response Syntax
#
#         {
#             'AnalysisSummaryList': [
#                 {
#                     'Arn': 'string',
#                     'AnalysisId': 'string',
#                     'Name': 'string',
#                     'Status': 'CREATION_IN_PROGRESS'|'CREATION_SUCCESSFUL'|'CREATION_FAILED'|'UPDATE_IN_PROGRESS'|'UPDATE_SUCCESSFUL'|'UPDATE_FAILED'|'DELETED',
#                     'CreatedTime': datetime(2015, 1, 1),
#                     'LastUpdatedTime': datetime(2015, 1, 1)
#                 },
#             ],
#             'NextToken': 'string',
#             'Status': 123,
#             'RequestId': 'string'
#         }
#
#         Response Structure
#
#             (dict) --
#
#                 AnalysisSummaryList (list) --
#
#                 Metadata describing each of the analyses that are listed.
#
#                     (dict) --
#
#                     The summary metadata that describes an analysis.
#
#                         Arn (string) --
#
#                         The Amazon Resource Name (ARN) for the analysis.
#
#                         AnalysisId (string) --
#
#                         The ID of the analysis. This ID displays in the URL.
#
#                         Name (string) --
#
#                         The name of the analysis. This name is displayed in the Amazon QuickSight console.
#
#                         Status (string) --
#
#                         The last known status for the analysis.
#
#                         CreatedTime (datetime) --
#
#                         The time that the analysis was created.
#
#                         LastUpdatedTime (datetime) --
#
#                         The time that the analysis was last updated.
#
#                 NextToken (string) --
#
#                 A pagination token that can be used in a subsequent request.
#
#                 Status (integer) --
#
#                 The HTTP status of the request.
#
#                 RequestId (string) --
#
#                 The Amazon Web Services request ID for this operation.
#
#     Exceptions
#
#         QuickSight.Client.exceptions.ThrottlingException
#         QuickSight.Client.exceptions.InvalidNextTokenException
#         QuickSight.Client.exceptions.UnsupportedUserEditionException
#         QuickSight.Client.exceptions.InternalFailureException

class QuickSightAnalysisProvider:
    def __init__(self):
        self._client = get_quicksight_client()

    def get_analysis_list(self):
        analyses = self._client.list_analyses(AwsAccountId=settings.AWS_ACCOUNT_ID)
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
        return analyses

    def get_analysis_url(self, analysis_id):
        analysis_url = self._client.get_analysis_embed_url(
            AwsAccountId=settings.AWS_ACCOUNT_ID,
            AnalysisId=analysis_id,
            IdentityType="IAM",
            SessionLifetimeInMinutes=1000,
            UndoRedoDisabled=True,
            ResetDisabled=True,
        )
        # Response example:
        # {
        #   "ResponseMetadata": {
        #     "RequestId": "a1f364ae-26c6-42e4-8a56-fa83299390e8",
        #     "HTTPStatusCode": 200,
        #     "HTTPHeaders": {
        #       "date": "Thu, 15 Dec 2022 17:02:28 GMT",
        #       "content-type": "application/json",
        #       "content-length": "95",
        #       "connection": "keep-alive",
        #       "x-amzn-requestid": "a1f364ae-26c6-42e4-8a56-fa83299390e8"
        #     },
        #     "RetryAttempts": 0
        #   },
        #   "EmbedUrl": "https://quicksight.aws.amazon.com/sn/dashboards/12345678-1234-1234-1234-123456789012?isauthcode=true&identitytype=IAM&sessionlifetime=1000&undo_redo_disabled=true&reset_disabled=true&...",
        #   "Status": 200,
        #   "RequestId": "a1f364ae-26c6-42e4-8a56-fa83299390e8"
        # }
        return analysis_url





