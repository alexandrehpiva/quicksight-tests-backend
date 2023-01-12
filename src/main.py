from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.settings import (
    BASE_PATH
)

from src import __version__
from src.providers.quicksight import (
    QuickSightDashboardProvider,
    QuickSightAnalysisProvider,
    QuickSightEmbeddingProvider,
    QuickSightUserProvider,
)

print(f"Starting app with path: {BASE_PATH}")

app = FastAPI(
    title="Quicksight API",
    description="Quicksight API",
    version=__version__,
    docs_url=f"{BASE_PATH}/docs",
    redoc_url=f"{BASE_PATH}/redoc",
    openapi_url=f"{BASE_PATH}/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(
#     router,
#     prefix=BASE_PATH,
#     tags=["quicksight"],
# )

@app.get("/")
async def health_check():
    return {"status": "ok"}


# QuickSight API

@app.get("/quicksight/dashboards")
async def get_dashboard_list():
    return QuickSightDashboardProvider().get_dashboard_list()


@app.get("/quicksight/analyses")
async def get_analysis_list():
    return QuickSightAnalysisProvider().get_analysis_list()


@app.get("/quicksight/dashboards/embedding_url_anonymous_user/{dashboard_id}")
async def get_dashboard_embedding_url(dashboard_id: str, session_tags: str = None):
    return QuickSightEmbeddingProvider().get_dashboard_embedding_url_for_anonymous_user(
        dashboard_id,
        session_tags.split(",") if session_tags else None,
    )

@app.get("/quicksight/dashboards/embedding_url/{dashboard_id}")
async def get_dashboard_embedding_url(
    dashboard_id: str,
    user_arn: str = None,
    user_name: str = None,
):
    return QuickSightEmbeddingProvider().get_dashboard_embedding_url_for_registered_user(
        dashboard_id,
        user_arn,
        user_name,
    )

@app.get("/quicksight/users")
async def get_user_list():
    return QuickSightUserProvider().get_user_list()