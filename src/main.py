from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.providers.quicksight import (
    QuickSightDashboardProvider,
    QuickSightAnalysisProvider,
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


@app.get("/quicksight/dashboards/{dashboard_id}")
async def get_dashboard_url(dashboard_id: str):
    url = QuickSightDashboardProvider().get_dashboard_url(dashboard_id)
    return {"url": url}


@app.get("/quicksight/analyses")
async def get_analysis_list():
    analyses = QuickSightAnalysisProvider().get_analysis_list()
    return analyses


@app.get("/quicksight/analyses/{analysis_id}")
async def get_analysis_url(analysis_id: str):
    url = QuickSightAnalysisProvider().get_analysis_url(analysis_id)
    return {"url": url}