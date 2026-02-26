from app.auth.dev_auth import dev_auth
from app.auth.appwrite_auth import appwrite_auth

from app.core.config import config

#   "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiI2OTdmMjY1OTAwMDZiNjRiN2E4OSIsInNlc3Npb25JZCI6IjY5YTAzYWZhYzc0ODk3MWJmZDA2IiwiZXhwIjoxNzcyMTA5NDkzfQ.8Rs96E6lYXciD_xMBuosDPjrzdD2LfXkKPsgurFg33k"

ENV = config.ENV

def get_auth_dependency():
    if ENV == "dev":
        return dev_auth

    return appwrite_auth


get_current_user = get_auth_dependency()