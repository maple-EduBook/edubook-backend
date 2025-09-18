import os

from fastapi import Request, HTTPException
from firebase_admin import auth
from jose import jwt


def get_user_info_by_request(request: Request):
    headers = request.headers
    token = headers.get('authorization').removeprefix('Bearer ')

    try:
        email = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])["email"]
    except:
        raise HTTPException(
            status_code=400, detail="Invalid Token"
        )

    try:
        user = auth.get_user_by_email(email)
    except:
        raise HTTPException(
            status_code=400, detail="Invalid Token"
        )

    return {"uid": user.uid}