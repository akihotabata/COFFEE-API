CREATE TABLE countries (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(2) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    name_local VARCHAR(100),
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE regions (
    id BIGSERIAL PRIMARY KEY,
    country_id BIGINT REFERENCES countries(id),
    name VARCHAR(100) NOT NULL,
    alt_name VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE subregions (
    id BIGSERIAL PRIMARY KEY,
    region_id BIGINT REFERENCES regions(id),
    name VARCHAR(100) NOT NULL,
    alt_name VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE producers (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    organization VARCHAR(150),
    country_id BIGINT REFERENCES countries(id),
    contact_json JSONB,
    notes TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE farms (
    id BIGSERIAL PRIMARY KEY,
    subregion_id BIGINT REFERENCES subregions(id),
    name VARCHAR(150) NOT NULL,
    alt_name VARCHAR(150),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    elevation_min_m INT,
    elevation_max_m INT,
    size_hectares DECIMAL(6,2),
    established_year SMALLINT,
    description TEXT,
    website VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE farm_producers (
    farm_id BIGINT REFERENCES farms(id),
    producer_id BIGINT REFERENCES producers(id),
    PRIMARY KEY (farm_id, producer_id)
);

CREATE TABLE varieties (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    family VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE processes (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE lots (
    id BIGSERIAL PRIMARY KEY,
    farm_id BIGINT REFERENCES farms(id),
    code VARCHAR(100) UNIQUE,
    harvest_year SMALLINT NOT NULL CHECK (harvest_year >= 1900 AND harvest_year <= 2100),
    crop_year VARCHAR(9),
    elevation_m INT,
    screen_size VARCHAR(10),
    process_id BIGINT REFERENCES processes(id),
    moisture_percent DECIMAL(4,2) CHECK (moisture_percent >= 0 AND moisture_percent <= 20),
    water_activity DECIMAL(4,3) CHECK (water_activity >= 0.40 AND water_activity <= 0.70),
    quantity_bags INT,
    bag_weight_kg DECIMAL(5,2),
    exporter VARCHAR(150),
    importer VARCHAR(150),
    description TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE lot_varieties (
    lot_id BIGINT REFERENCES lots(id),
    variety_id BIGINT REFERENCES varieties(id),
    ratio_pct DECIMAL(5,2) CHECK (ratio_pct >= 0 AND ratio_pct <= 100),
    PRIMARY KEY (lot_id, variety_id)
);

CREATE TABLE tasting_notes (
    id BIGSERIAL PRIMARY KEY,
    category VARCHAR(50),
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE lot_tasting_notes (
    lot_id BIGINT REFERENCES lots(id),
    tasting_note_id BIGINT REFERENCES tasting_notes(id),
    intensity SMALLINT CHECK (intensity >= 1 AND intensity <= 5),
    PRIMARY KEY (lot_id, tasting_note_id)
);

CREATE TABLE certifications (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE,
    name VARCHAR(150),
    description TEXT
);

CREATE TABLE farm_certifications (
    farm_id BIGINT REFERENCES farms(id),
    certification_id BIGINT REFERENCES certifications(id),
    valid_from DATE,
    valid_to DATE,
    PRIMARY KEY (farm_id, certification_id)
);

CREATE TABLE cupping_sessions (
    id BIGSERIAL PRIMARY KEY,
    lot_id BIGINT REFERENCES lots(id),
    session_date DATE NOT NULL,
    cupper_name VARCHAR(100),
    location VARCHAR(150),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE cupping_scores (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT REFERENCES cupping_sessions(id),
    aroma DECIMAL(4,2),
    flavor DECIMAL(4,2),
    acidity DECIMAL(4,2),
    body DECIMAL(4,2),
    balance DECIMAL(4,2),
    aftertaste DECIMAL(4,2),
    uniformity DECIMAL(4,2),
    clean_cup DECIMAL(4,2),
    sweetness DECIMAL(4,2),
    total_score DECIMAL(5,2) CHECK (total_score >= 0 AND total_score <= 100)
);
