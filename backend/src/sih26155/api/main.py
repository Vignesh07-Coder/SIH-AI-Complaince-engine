from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sih26155.api.routes.analysis import router as analysis_router


app = FastAPI(
    title="SIH AI Compliance Engine",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(analysis_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
