import uuid
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.schemas.analyze import StockRequest, AnalyzeResponse
from app.db.session import get_db, AsyncSessionLocal
from app.repositories.workflow_repository import create_run, update_run_complete, update_run_failed
from app.workflows.orchestrator import run_stock_workflow

router = APIRouter()


async def run_workflow_task(run_id: str, ticker: str, analysis_type: str, risk_tolerance: str):
    async with AsyncSessionLocal() as db:
        try:
            logger.info(f"Background task started for run_id: {run_id}")
            plan = run_stock_workflow(ticker, analysis_type, risk_tolerance)
            await update_run_complete(db, run_id, plan)
            logger.info(f"Background task complete for run_id: {run_id}")
        except Exception as e:
            logger.error(f"Background task failed for run_id {run_id}: {e}")
            await update_run_failed(db, run_id, str(e))


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    request: StockRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    run_id = str(uuid.uuid4())

    await create_run(db, run_id, request.ticker, request.analysis_type, request.risk_tolerance)

    background_tasks.add_task(
        run_workflow_task,
        run_id,
        request.ticker,
        request.analysis_type,
        request.risk_tolerance,
    )

    return AnalyzeResponse(
        id=run_id,
        status="pending",
        message=f"Analysis started for {request.ticker}. Poll GET /results/{run_id} for results.",
    )