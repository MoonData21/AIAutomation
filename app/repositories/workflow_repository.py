import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.workflow_run import WorkflowRun
from app.schemas.analyze import StockAnalysis


async def create_run(db: AsyncSession, run_id: str, ticker: str, analysis_type: str, risk_tolerance: str) -> WorkflowRun:
    run = WorkflowRun(
        id=run_id,
        ticker=ticker,
        analysis_type=analysis_type,
        risk_tolerance=risk_tolerance,
        status="pending",
    )
    db.add(run)
    await db.commit()
    await db.refresh(run)
    return run


async def update_run_complete(db: AsyncSession, run_id: str, plan: StockAnalysis) -> None:
    result = await db.execute(select(WorkflowRun).where(WorkflowRun.id == run_id))
    run = result.scalar_one_or_none()
    if run:
        run.status = "complete"
        run.result_json = json.dumps(plan.model_dump())
        await db.commit()


async def update_run_failed(db: AsyncSession, run_id: str, error: str) -> None:
    result = await db.execute(select(WorkflowRun).where(WorkflowRun.id == run_id))
    run = result.scalar_one_or_none()
    if run:
        run.status = "failed"
        run.error = error
        await db.commit()


async def get_run(db: AsyncSession, run_id: str) -> WorkflowRun | None:
    result = await db.execute(select(WorkflowRun).where(WorkflowRun.id == run_id))
    return result.scalar_one_or_none()