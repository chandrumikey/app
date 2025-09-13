from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app .models import usermodel as models
from app.crud import taskcrud as crud
from app.core.database import get_db
from app.core.auth import get_current_active_user

def get_task_or_404(
    task_id: int, 
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    task = crud.get_task(db, task_id=task_id, user_id=current_user.id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task