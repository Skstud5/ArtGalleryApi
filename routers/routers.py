from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from data_base.database import get_db
from models.models import User, Image, Comment
from models.schemas import UserCreate, UserResponse, ImageCreate, ImageResponse, CommentCreate, CommentResponse
from security.security import get_current_user, create_access_token, authenticate_user, get_password_hash

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/images/", response_model=ImageResponse)
def create_image(image: ImageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # TODO Пишет, что The `dict` method is deprecated; use `model_dump` instead.
    # db_image = Image(**image.dict(), uploaded_by=current_user.id)
    # TODO возможно, что нужно использовать такой вариант:
    db_image = Image(**image.model_dump(), uploaded_by=current_user.id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


@router.get("/images/{image_id}", response_model=ImageResponse)
def read_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image


@router.post("/comments/", response_model=CommentResponse)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    # TODO Пишет, что The `dict` method is deprecated; use `model_dump` instead.
    # db_comment = Comment(**comment.dict(), user_id=current_user.id)
    db_comment = Comment(**comment.model_dump(), user_id=current_user.id)
    # TODO возможно, что нужно использовать такой вариант:
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
