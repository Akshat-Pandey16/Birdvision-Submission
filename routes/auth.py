from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from models.db import get_db, User
from models.models import SignUpModel
from resource.auth_helper import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

router = APIRouter(tags=["auth"])


@router.post("/signup")
def signup(signup_data: SignUpModel, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.

    Parameters:
    - `signup_data` (SignUpModel): Data containing username, email, and password.
        - username (str): Username.
        - email (str): Email (should adhere to email standards).
        - password (str): Password. (should be at least 8 characters long, with combination of letters, numbers, and special characters)

    Returns:
    - `msg` (str): Success message.
    """
    username = signup_data.username
    email = signup_data.email
    password = signup_data.password
    user_exist = get_user(db=db, username=username)
    if user_exist:
        raise HTTPException(status_code=400, detail="Username already registered")
    pwd_hash = get_password_hash(password)
    new_user = User(username=username, email=email, hashed_password=pwd_hash)
    db.add(new_user)
    db.commit()
    return {"msg": "User created successfully"}


@router.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Endpoint to login and get an access token.

    Parameters:
    - `form_data` (OAuth2PasswordRequestForm): Form data containing username and password.
    
    Returns:
    - `access_token` (str): JWT access token.
    - `token_type` (str): Token type.
    """
    username = form_data.username
    password = form_data.password
    user = authenticate_user(
        db=db,
        username=username,
        password=password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
