from fastapi import Depends, HTTPException, status
from jose import JOSEError, JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, model,config
from .database import get_db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key, algorithm, expriation time

SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorihm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.expire


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # jwt.encode(update copy of payload(data),secret key,algorithm)

    encodec_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encodec_jwt


def verify_access_token(token: str, credentials_exception):
    print(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        idd: str = payload.get("user_id")

        if idd is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=idd)
    except JWTError:
        raise credentials_exception
    print(token_data)
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception=credentials_exception)
    user = db.query(model.User).filter(model.User.id == token.id).first()
    return user
