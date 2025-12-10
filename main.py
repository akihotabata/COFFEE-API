from fastapi import FastAPI

import models
from database import engine
from routers import certification, country, cupping_score, cupping_session, farm, lot, process, producer, region, subregion, tasting_note, variety

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="World Coffee Farm API", version="1.0")

app.include_router(country.router, prefix="/api/v1")
app.include_router(region.router, prefix="/api/v1")
app.include_router(subregion.router, prefix="/api/v1")
app.include_router(farm.router, prefix="/api/v1")
app.include_router(producer.router, prefix="/api/v1")
app.include_router(lot.router, prefix="/api/v1")
app.include_router(variety.router, prefix="/api/v1")
app.include_router(process.router, prefix="/api/v1")
app.include_router(tasting_note.router, prefix="/api/v1")
app.include_router(cupping_session.router, prefix="/api/v1")
app.include_router(cupping_score.router, prefix="/api/v1")
app.include_router(certification.router, prefix="/api/v1")
