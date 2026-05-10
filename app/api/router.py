from fastapi import APIRouter
from app.api.routes import health, analyze, results

router = APIRouter()

router.include_router(health.router, tags=["Health"])
router.include_router(analyze.router, tags=["Analyze"])
router.include_router(results.router, tags=["Results"])