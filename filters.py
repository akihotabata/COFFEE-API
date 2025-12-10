from sqlalchemy.orm import Session

from models import (
    Country,
    CuppingScore,
    CuppingSession,
    Farm,
    Lot,
    LotTastingNote,
    LotVariety,
    Region,
    Subregion,
    TastingNote,
)
from schemas import FarmSearchParams, LotSearchParams


def filter_farms(db: Session, params: FarmSearchParams):
    query = db.query(Farm)
    if params.subregion_id:
        query = query.filter(Farm.subregion_id == params.subregion_id)
    elif params.region_id:
        query = query.join(Subregion).filter(Subregion.region_id == params.region_id)
    elif params.country_code:
        query = (
            query.join(Subregion)
            .join(Region)
            .join(Country, Region.country_id == Country.id)
            .filter(Country.code == params.country_code)
        )

    if params.min_altitude is not None:
        query = query.filter(Farm.elevation_max_m >= params.min_altitude)
    if params.max_altitude is not None:
        query = query.filter(Farm.elevation_min_m <= params.max_altitude)
    if params.q:
        like = f"%{params.q}%"
        query = query.filter((Farm.name.ilike(like)) | (Farm.description.ilike(like)))

    total = query.count()
    items = (
        query.offset((params.page - 1) * params.per_page)
        .limit(params.per_page)
        .all()
    )
    return total, items


def filter_lots(db: Session, params: LotSearchParams):
    query = db.query(Lot)

    if params.farm_id:
        query = query.filter(Lot.farm_id == params.farm_id)
    if params.country_code:
        query = (
            query.join(Lot.farm)
            .join(Farm.subregion)
            .join(Subregion.region)
            .join(Country, Region.country_id == Country.id)
            .filter(Country.code == params.country_code)
        )
    if params.variety_id:
        query = query.join(LotVariety).filter(LotVariety.variety_id == params.variety_id)
    if params.process_id:
        query = query.filter(Lot.process_id == params.process_id)
    if params.harvest_year:
        query = query.filter(Lot.harvest_year == params.harvest_year)
    if params.min_altitude is not None:
        query = query.filter(Lot.elevation_m >= params.min_altitude)
    if params.max_altitude is not None:
        query = query.filter(Lot.elevation_m <= params.max_altitude)
    if params.tasting:
        like = f"%{params.tasting}%"
        query = query.join(LotTastingNote).join(TastingNote).filter(TastingNote.name.ilike(like))
    if params.min_score is not None or params.max_score is not None:
        query = query.join(CuppingSession).join(CuppingScore)
        if params.min_score is not None:
            query = query.filter(CuppingScore.total_score >= params.min_score)
        if params.max_score is not None:
            query = query.filter(CuppingScore.total_score <= params.max_score)

    total = query.count()
    items = (
        query.offset((params.page - 1) * params.per_page)
        .limit(params.per_page)
        .all()
    )
    return total, items
