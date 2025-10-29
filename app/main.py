from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from datetime import date
from typing import List
import uvicorn
from .schemas import CapacityResponse
from .queries import GET_CAPACITY_QUERY


# DB setup and FastAPI app
app = FastAPI()
DATABASE_URL = "sqlite:///app/data.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API endpoint to get capacity data
@app.get("/capacity", response_model=List[CapacityResponse])
async def get_capacity(
    date_from: date = Query("2024-01-01"),
    date_to: date = Query("2024-03-31"),
    db: Session = Depends(get_db),
):
    if date_from > date_to:
        raise HTTPException(status_code=400, detail="date_from cannot be after date_to")

    query = text(GET_CAPACITY_QUERY)
    result = db.execute(
        query, {"date_from": date_from.isoformat(), "date_to": date_to.isoformat()}
    )

    rows = result.fetchall()
    return [
        CapacityResponse(
            week_start_date=row[0],
            week_no=row[1],
            offered_capacity_teu=row[2],
        )
        for row in rows
    ]


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
