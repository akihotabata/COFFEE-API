from datetime import datetime
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    DECIMAL,
    ForeignKey,
    Integer,
    JSON,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(BigInteger, primary_key=True, index=True)
    code = Column(String(2), nullable=False)
    name_en = Column(String(100), nullable=False)
    name_local = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    regions = relationship("Region", back_populates="country", cascade="all, delete-orphan")


class Region(Base):
    __tablename__ = "regions"

    id = Column(BigInteger, primary_key=True, index=True)
    country_id = Column(BigInteger, ForeignKey("countries.id"))
    name = Column(String(100), nullable=False)
    alt_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    country = relationship("Country", back_populates="regions")
    subregions = relationship("Subregion", back_populates="region", cascade="all, delete-orphan")


class Subregion(Base):
    __tablename__ = "subregions"

    id = Column(BigInteger, primary_key=True, index=True)
    region_id = Column(BigInteger, ForeignKey("regions.id"))
    name = Column(String(100), nullable=False)
    alt_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    region = relationship("Region", back_populates="subregions")
    farms = relationship("Farm", back_populates="subregion", cascade="all, delete-orphan")


class Producer(Base):
    __tablename__ = "producers"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    organization = Column(String(150))
    country_id = Column(BigInteger, ForeignKey("countries.id"))
    contact_json = Column(JSON)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    farms = relationship("FarmProducer", back_populates="producer", cascade="all, delete-orphan")


class Farm(Base):
    __tablename__ = "farms"

    id = Column(BigInteger, primary_key=True, index=True)
    subregion_id = Column(BigInteger, ForeignKey("subregions.id"))
    name = Column(String(150), nullable=False)
    alt_name = Column(String(150))
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))
    elevation_min_m = Column(Integer)
    elevation_max_m = Column(Integer)
    size_hectares = Column(DECIMAL(6, 2))
    established_year = Column(SmallInteger)
    description = Column(Text)
    website = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subregion = relationship("Subregion", back_populates="farms")
    lots = relationship("Lot", back_populates="farm", cascade="all, delete-orphan")
    producers = relationship("FarmProducer", back_populates="farm", cascade="all, delete-orphan")
    certifications = relationship("FarmCertification", back_populates="farm", cascade="all, delete-orphan")


class FarmProducer(Base):
    __tablename__ = "farm_producers"
    __table_args__ = (
        UniqueConstraint("farm_id", "producer_id", name="pk_farm_producers"),
    )

    farm_id = Column(BigInteger, ForeignKey("farms.id"), primary_key=True)
    producer_id = Column(BigInteger, ForeignKey("producers.id"), primary_key=True)

    farm = relationship("Farm", back_populates="producers")
    producer = relationship("Producer", back_populates="farms")


class Variety(Base):
    __tablename__ = "varieties"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    family = Column(String(100))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lot_varieties = relationship("LotVariety", back_populates="variety", cascade="all, delete-orphan")


class Process(Base):
    __tablename__ = "processes"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lots = relationship("Lot", back_populates="process", cascade="all, delete-orphan")


class Lot(Base):
    __tablename__ = "lots"

    id = Column(BigInteger, primary_key=True, index=True)
    farm_id = Column(BigInteger, ForeignKey("farms.id"))
    code = Column(String(100), unique=True)
    harvest_year = Column(SmallInteger, nullable=False)
    crop_year = Column(String(9))
    elevation_m = Column(Integer)
    screen_size = Column(String(10))
    process_id = Column(BigInteger, ForeignKey("processes.id"))
    moisture_percent = Column(DECIMAL(4, 2))
    water_activity = Column(DECIMAL(4, 3))
    quantity_bags = Column(Integer)
    bag_weight_kg = Column(DECIMAL(5, 2))
    exporter = Column(String(150))
    importer = Column(String(150))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    farm = relationship("Farm", back_populates="lots")
    process = relationship("Process", back_populates="lots")
    varieties = relationship("LotVariety", back_populates="lot", cascade="all, delete-orphan")
    tasting_notes = relationship("LotTastingNote", back_populates="lot", cascade="all, delete-orphan")
    cupping_sessions = relationship("CuppingSession", back_populates="lot", cascade="all, delete-orphan")


class LotVariety(Base):
    __tablename__ = "lot_varieties"
    __table_args__ = (
        UniqueConstraint("lot_id", "variety_id", name="pk_lot_varieties"),
    )

    lot_id = Column(BigInteger, ForeignKey("lots.id"), primary_key=True)
    variety_id = Column(BigInteger, ForeignKey("varieties.id"), primary_key=True)
    ratio_pct = Column(DECIMAL(5, 2))

    lot = relationship("Lot", back_populates="varieties")
    variety = relationship("Variety", back_populates="lot_varieties")


class TastingNote(Base):
    __tablename__ = "tasting_notes"

    id = Column(BigInteger, primary_key=True, index=True)
    category = Column(String(50))
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lot_tasting_notes = relationship("LotTastingNote", back_populates="tasting_note", cascade="all, delete-orphan")


class LotTastingNote(Base):
    __tablename__ = "lot_tasting_notes"
    __table_args__ = (
        UniqueConstraint("lot_id", "tasting_note_id", name="pk_lot_tasting_notes"),
        CheckConstraint("intensity >= 1 AND intensity <= 5", name="ck_intensity_range"),
    )

    lot_id = Column(BigInteger, ForeignKey("lots.id"), primary_key=True)
    tasting_note_id = Column(BigInteger, ForeignKey("tasting_notes.id"), primary_key=True)
    intensity = Column(SmallInteger)

    lot = relationship("Lot", back_populates="tasting_notes")
    tasting_note = relationship("TastingNote", back_populates="lot_tasting_notes")


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(BigInteger, primary_key=True, index=True)
    code = Column(String(20), unique=True)
    name = Column(String(150))
    description = Column(Text)

    farm_certifications = relationship("FarmCertification", back_populates="certification", cascade="all, delete-orphan")


class FarmCertification(Base):
    __tablename__ = "farm_certifications"
    __table_args__ = (
        UniqueConstraint("farm_id", "certification_id", name="pk_farm_certifications"),
    )

    farm_id = Column(BigInteger, ForeignKey("farms.id"), primary_key=True)
    certification_id = Column(BigInteger, ForeignKey("certifications.id"), primary_key=True)
    valid_from = Column(Date)
    valid_to = Column(Date)

    farm = relationship("Farm", back_populates="certifications")
    certification = relationship("Certification", back_populates="farm_certifications")


class CuppingSession(Base):
    __tablename__ = "cupping_sessions"

    id = Column(BigInteger, primary_key=True, index=True)
    lot_id = Column(BigInteger, ForeignKey("lots.id"))
    session_date = Column(Date, nullable=False)
    cupper_name = Column(String(100))
    location = Column(String(150))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lot = relationship("Lot", back_populates="cupping_sessions")
    scores = relationship("CuppingScore", back_populates="session", cascade="all, delete-orphan")


class CuppingScore(Base):
    __tablename__ = "cupping_scores"

    id = Column(BigInteger, primary_key=True, index=True)
    session_id = Column(BigInteger, ForeignKey("cupping_sessions.id"))
    aroma = Column(DECIMAL(4, 2))
    flavor = Column(DECIMAL(4, 2))
    acidity = Column(DECIMAL(4, 2))
    body = Column(DECIMAL(4, 2))
    balance = Column(DECIMAL(4, 2))
    aftertaste = Column(DECIMAL(4, 2))
    uniformity = Column(DECIMAL(4, 2))
    clean_cup = Column(DECIMAL(4, 2))
    sweetness = Column(DECIMAL(4, 2))
    total_score = Column(DECIMAL(5, 2))

    session = relationship("CuppingSession", back_populates="scores")
