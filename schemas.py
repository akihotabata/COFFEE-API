from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class CountryBase(BaseModel):
    code: str
    name_en: str
    name_local: Optional[str] = None


class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    pass


class Country(CountryBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class RegionBase(BaseModel):
    country_id: Optional[int] = None
    name: str
    alt_name: Optional[str] = None


class RegionCreate(RegionBase):
    pass


class RegionUpdate(RegionBase):
    pass


class Region(RegionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class SubregionBase(BaseModel):
    region_id: Optional[int] = None
    name: str
    alt_name: Optional[str] = None


class SubregionCreate(SubregionBase):
    pass


class SubregionUpdate(SubregionBase):
    pass


class Subregion(SubregionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ProducerBase(BaseModel):
    name: str
    organization: Optional[str] = None
    country_id: Optional[int] = None
    contact_json: Optional[dict] = None
    notes: Optional[str] = None


class ProducerCreate(ProducerBase):
    pass


class ProducerUpdate(ProducerBase):
    pass


class Producer(ProducerBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class FarmBase(BaseModel):
    subregion_id: Optional[int] = None
    name: str
    alt_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation_min_m: Optional[int] = None
    elevation_max_m: Optional[int] = None
    size_hectares: Optional[float] = None
    established_year: Optional[int] = None
    description: Optional[str] = None
    website: Optional[str] = None


class FarmCreate(FarmBase):
    pass


class FarmUpdate(FarmBase):
    pass


class Farm(FarmBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class FarmProducerBase(BaseModel):
    farm_id: int
    producer_id: int


class FarmProducerCreate(FarmProducerBase):
    pass


class FarmProducer(FarmProducerBase):
    class Config:
        orm_mode = True


class VarietyBase(BaseModel):
    name: str
    family: Optional[str] = None
    description: Optional[str] = None


class VarietyCreate(VarietyBase):
    pass


class VarietyUpdate(VarietyBase):
    pass


class Variety(VarietyBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ProcessBase(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None


class ProcessCreate(ProcessBase):
    pass


class ProcessUpdate(ProcessBase):
    pass


class Process(ProcessBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class LotBase(BaseModel):
    farm_id: Optional[int] = None
    code: Optional[str] = None
    harvest_year: int = Field(..., ge=1900, le=2100)
    crop_year: Optional[str] = None
    elevation_m: Optional[int] = None
    screen_size: Optional[str] = None
    process_id: Optional[int] = None
    moisture_percent: Optional[float] = Field(None, ge=0, le=20)
    water_activity: Optional[float] = Field(None, ge=0.40, le=0.70)
    quantity_bags: Optional[int] = None
    bag_weight_kg: Optional[float] = None
    exporter: Optional[str] = None
    importer: Optional[str] = None
    description: Optional[str] = None


class LotCreate(LotBase):
    pass


class LotUpdate(LotBase):
    pass


class Lot(LotBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class LotVarietyBase(BaseModel):
    lot_id: int
    variety_id: int
    ratio_pct: Optional[float] = Field(None, ge=0, le=100)


class LotVarietyCreate(LotVarietyBase):
    pass


class LotVariety(LotVarietyBase):
    class Config:
        orm_mode = True


class TastingNoteBase(BaseModel):
    category: Optional[str] = None
    name: str


class TastingNoteCreate(TastingNoteBase):
    pass


class TastingNoteUpdate(TastingNoteBase):
    pass


class TastingNote(TastingNoteBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class LotTastingNoteBase(BaseModel):
    lot_id: int
    tasting_note_id: int
    intensity: int = Field(..., ge=1, le=5)


class LotTastingNoteCreate(LotTastingNoteBase):
    pass


class LotTastingNote(LotTastingNoteBase):
    class Config:
        orm_mode = True


class CertificationBase(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(CertificationBase):
    pass


class Certification(CertificationBase):
    id: int

    class Config:
        orm_mode = True


class FarmCertificationBase(BaseModel):
    farm_id: int
    certification_id: int
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None


class FarmCertificationCreate(FarmCertificationBase):
    pass


class FarmCertification(FarmCertificationBase):
    class Config:
        orm_mode = True


class CuppingSessionBase(BaseModel):
    lot_id: Optional[int] = None
    session_date: date
    cupper_name: Optional[str] = None
    location: Optional[str] = None


class CuppingSessionCreate(CuppingSessionBase):
    pass


class CuppingSessionUpdate(CuppingSessionBase):
    pass


class CuppingSession(CuppingSessionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class CuppingScoreBase(BaseModel):
    session_id: int
    aroma: Optional[float] = None
    flavor: Optional[float] = None
    acidity: Optional[float] = None
    body: Optional[float] = None
    balance: Optional[float] = None
    aftertaste: Optional[float] = None
    uniformity: Optional[float] = None
    clean_cup: Optional[float] = None
    sweetness: Optional[float] = None
    total_score: Optional[float] = Field(None, ge=0, le=100)


class CuppingScoreCreate(CuppingScoreBase):
    pass


class CuppingScoreUpdate(CuppingScoreBase):
    pass


class CuppingScore(CuppingScoreBase):
    id: int

    class Config:
        orm_mode = True


class Pagination(BaseModel):
    page: int = 1
    per_page: int = 50


class FarmSearchParams(Pagination):
    country_code: Optional[str] = None
    region_id: Optional[int] = None
    subregion_id: Optional[int] = None
    min_altitude: Optional[int] = None
    max_altitude: Optional[int] = None
    q: Optional[str] = None


class LotSearchParams(Pagination):
    country_code: Optional[str] = None
    farm_id: Optional[int] = None
    variety_id: Optional[int] = None
    process_id: Optional[int] = None
    harvest_year: Optional[int] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None
    tasting: Optional[str] = None
    min_altitude: Optional[int] = None
    max_altitude: Optional[int] = None


class PaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    items: List

    class Config:
        arbitrary_types_allowed = True
