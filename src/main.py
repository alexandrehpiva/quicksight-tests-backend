from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.providers.quicksight import (
    QuickSightDashboardProvider,
    QuickSightAnalysisProvider,
    QuickSightEmbeddingProvider,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    return {"status": "ok"}


# QuickSight API

@app.get("/quicksight/dashboards")
async def get_dashboard_list():
    dashboards = QuickSightDashboardProvider().get_dashboard_list()
    return dashboards


@app.get("/quicksight/analyses")
async def get_analysis_list():
    analyses = QuickSightAnalysisProvider().get_analysis_list()
    return analyses


@app.get("/quicksight/embedding")
async def get_embedding_url(dashboard_id: str, analysis_id: str):
    embedding_url = QuickSightEmbeddingProvider().get_embedding_url(
        dashboard_id, analysis_id
    )
    return embedding_url