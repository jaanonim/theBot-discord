import os


def getToken():
    token = os.getenv("TOKEN")
    if not token:
        with open("token.txt") as f:
            token = f.read()
    return token
