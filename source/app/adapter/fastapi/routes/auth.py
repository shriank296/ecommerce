from fastapi import APIRouter, Form, Depends, HTTPException
from source.app.adapter.fastapi.dependencies import get_repos, get_token_service
from source.app.ports.db.repositories import Repositories

router = APIRouter()

@router.post('/')
def login(email: str = Form(...), password: str = Form(...),repos: Repositories = Depends(get_repos), jwt_service= Depends(get_token_service)):
    user_repo = repos.user
    user = user_repo.get_autheticated_user(email, password)
    if user:
        token = jwt_service.create_token(user_name=email, role = user.role)
        return {"token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credential")




