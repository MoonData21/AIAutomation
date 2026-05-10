import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.result import WorkflowResult
from app.schemas.analyze import StockAnalysis
from app.db.session import get_db
from app.repositories.workflow_repository import get_run

router = APIRouter()


@router.get("/results/{run_id}", response_model=WorkflowResult)
async def get_results(run_id: str, db: AsyncSession = Depends(get_db)):
    run = await get_run(db, run_id)

    if not run:
        raise HTTPException(status_code=404, detail=f"No workflow found with id: {run_id}")

    result = None
    if run.status == "complete" and run.result_json:
        result = StockAnalysis(**json.loads(run.result_json))

    return WorkflowResult(
        id=run.id,
        status=run.status,
        ticker=run.ticker,
        result=result,
        error=run.error,
    )