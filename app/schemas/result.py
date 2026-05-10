from pydantic import BaseModel
from typing import Optional
from app.schemas.analyze import StockAnalysis


class WorkflowResult(BaseModel):
    id: str
    status: str
    ticker: str
    result: Optional[StockAnalysis] = None
    error: Optional[str] = None