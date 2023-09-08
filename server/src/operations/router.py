from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import insert

from src.database import session
from src.operations.models import reports
from src.operations.schemas import Report

router = APIRouter(
    prefix="/api",
    tags=["Api"]
)


@router.get("/image")
def get_image(image_path: str):
    return FileResponse(image_path)


@router.get("/reports")
def get_reports():
    try:
        results = session.query(reports).all()
        return {
            "status": "success",
            "data": [result._asdict() for result in results],
            "details": None
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("/report")
def add_report(new_report: Report):
    stmt = insert(reports).values(**new_report.dict())
    session.execute(stmt)
    session.commit()
    return {"status": "success"}

