import pathlib
import socket

from starlette.config import Config

config = Config()

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE_DIR = ROOT.parent

DEBUG = config('DEBUG', bool, False)

BASE_PATH = config('BASE_PATH', cast=str, default='/')
ENVIRONMENT = config('ENVIRONMENT', cast=str, default='dev')
HOSTNAME = config('HOSTNAME', str, socket.gethostname())
HOST = config('APP_DEFAULT_HOST', str, '0.0.0.0')
PORT = config('APP_DEFAULT_PORT', int, 8000)
WORKERS = config('APP_DEFAULT_WORKERS', int, 1)

# AWS config
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', cast=str, default=None)
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', cast=str, default=None)
AWS_DEFAULT_REGION = config('AWS_DEFAULT_REGION', cast=str, default='us-east-1')
AWS_ACCOUNT_ID = config('AWS_ACCOUNT_ID', cast=str, default=None)
