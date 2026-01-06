import os

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")
    CORS_ORIGINS = "*"
