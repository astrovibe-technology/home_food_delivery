from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, date

from database.db import get_db
from models.issue import Issue
from pydantic import BaseModel
from datetime import datetime,timedelta
from typing import Optional


router = APIRouter(prefix="/issue", tags=["Issue"])



class IssueCreate(BaseModel):
    user_id: int
    title: str
    description: str
    issue_type: Optional[str] = None

class IssueResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    issue_type: Optional[str]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True




# ✅ POST - Create Issue
@router.post("/", response_model=IssueResponse)
def create_issue(data: IssueCreate, db: Session = Depends(get_db)):
    new_issue = Issue(
        user_id=data.user_id,
        title=data.title,
        description=data.description,
        issue_type=data.issue_type,
        status="open",
        created_at=datetime.utcnow()
    )

    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    return new_issue


# ✅ GET - Issues List with STATUS + DATE FILTER (Inclusive 🔥)
@router.get("/", response_model=List[IssueResponse])
def get_issues(
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Issue)

    # 🔹 Filter by status
    if status:
        query = query.filter(Issue.status == status)

    # 🔹 Filter by start date
    if start_date:
        query = query.filter(Issue.created_at >= start_date)

    # 🔹 Filter by end date (IMPORTANT FIX 🔥)
    if end_date:
        query = query.filter(
            Issue.created_at < end_date + timedelta(days=1)
        )

    issues = query.order_by(Issue.id.desc()).all()

    return issues