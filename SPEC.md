【Codex 生成用】世界コーヒー農園データ API 完全仕様書

────────────────────────────────────

本仕様書は「世界中のコーヒー豆データを国 → 地域 → サブ地域 → 農園 → ロット → 品種／精製 → カッピング → フレーバーノート」まで管理する REST API を自動生成するための完全要件定義です。
前提として RDB（PostgreSQL推奨）＋ REST API（FastAPI を例と想定） を基本とし、Codex に投入すれば自動的にコードを生成できるよう、曖昧表現を排除した精密な仕様を記述しています。

1. システム概要（API の目的）

本 API は以下を実現するために設計する：

世界中のコーヒー豆の情報を階層構造で管理

国 (Country)

地域 (Region)

サブ地域 (Subregion)

農園 (Farm)

ロット (Lot)

品種 (Variety)

精製方法 (Process)

フレーバーノート (Tasting Note)

カッピングスコア (Cupping Score)

検索条件に応じて、高度なフィルタリングが可能

国 / 地域 / サブ地域による検索

標高帯検索

収穫年検索

品種・精製方法での絞り込み

カッピングスコアによるフィルタ

フレーバーノートを含むテキスト検索

将来的に以下との連携を前提：

ローストログ（Aillio Bullet R1）との紐づけ

抽出ログやブリュー記録との紐づけ

ユーザーのお気に入り機能

外部データインポート（COE/Cafe Imports/Nordic Approach）対応

2. 技術スタックの前提（Codex が理解しやすい前提）

本仕様では以下を想定する：

言語: Python 3.10+

Web フレームワーク: FastAPI

ORM: SQLAlchemy + Pydantic

DB: PostgreSQL

API形式: REST JSON

認証: なし（必要であれば JWT を後付け可能）

Codex には
「モデル定義 → CRUD → ルーター実装 → DB スキーマ → 初期データ投入」
まで生成させる。

3. ER 図（文章化・Codex解釈用）
Country 1 ── * Region 1 ── * Subregion 1 ── * Farm 1 ── * Lot
Farm * ── * Producer (farm_producers)
Lot * ── * Variety (lot_varieties)
Lot * ── * Process
Lot * ── * Tasting Note (lot_tasting_notes)
Lot 1 ── * Cupping Session ── * Cupping Score
Farm * ── * Certification (farm_certifications)


主キーは全て数値型（BIGINT）で統一。

4. テーブル定義（完全仕様：Codex が CREATE TABLE を生成できるレベル）

以下は 必ず PK/FK を含む、型も指定した完全仕様。

────────────────────────────

4.1 countries（国）
id: BIGINT PK
code: VARCHAR(2) NOT NULL  // ISO3166
name_en: VARCHAR(100) NOT NULL
name_local: VARCHAR(100)
created_at: TIMESTAMP DEFAULT now()
updated_at: TIMESTAMP DEFAULT now()


────────────────────────────

4.2 regions（地域）
id: BIGINT PK
country_id: BIGINT FK → countries(id)
name: VARCHAR(100) NOT NULL
alt_name: VARCHAR(100)
created_at: TIMESTAMP
updated_at: TIMESTAMP


────────────────────────────

4.3 subregions（サブ地域）
id: BIGINT PK
region_id: BIGINT FK → regions(id)
name: VARCHAR(100) NOT NULL
alt_name: VARCHAR(100)
created_at: TIMESTAMP
updated_at: TIMESTAMP


────────────────────────────

4.4 producers（生産者）
id: BIGINT PK
name: VARCHAR(150) NOT NULL
organization: VARCHAR(150)
country_id: BIGINT FK → countries(id)
contact_json: JSONB
notes: TEXT
created_at: TIMESTAMP
updated_at: TIMESTAMP


────────────────────────────

4.5 farms（農園）
id: BIGINT PK
subregion_id: BIGINT FK → subregions(id)
name: VARCHAR(150) NOT NULL
alt_name: VARCHAR(150)
latitude: DECIMAL(9,6)
longitude: DECIMAL(9,6)
elevation_min_m: INT
elevation_max_m: INT
size_hectares: DECIMAL(6,2)
established_year: SMALLINT
description: TEXT
website: VARCHAR(255)
created_at: TIMESTAMP
updated_at: TIMESTAMP


────────────────────────────

4.6 farm_producers（中間テーブル：農園-生産者）
farm_id: BIGINT FK → farms(id)
producer_id: BIGINT FK → producers(id)
PRIMARY KEY (farm_id, producer_id)


────────────────────────────

4.7 varieties（品種）
id: BIGINT PK
name: VARCHAR(100) NOT NULL
family: VARCHAR(100)
description: TEXT
created_at: TIMESTAMP
updated_at: TIMESTAMP


────────────────────────────

4.8 processes（精製方法）
id: BIGINT PK
name: VARCHAR(100) NOT NULL
category: VARCHAR(50)
description: TEXT
created_at: TIMESTAMP
updated_at: TIMESTAMP


────────────────────────────

4.9 lots（ロット）
id: BIGINT PK
farm_id: BIGINT FK → farms(id)
code: VARCHAR(100) UNIQUE
harvest_year: SMALLINT NOT NULL
crop_year: VARCHAR(9)
elevation_m: INT
screen_size: VARCHAR(10)
process_id: BIGINT FK → processes(id)
moisture_percent: DECIMAL(4,2)
water_activity: DECIMAL(4,3)
quantity_bags: INT
bag_weight_kg: DECIMAL(5,2)
exporter: VARCHAR(150)
importer: VARCHAR(150)
description: TEXT
created_at: TIMESTAMP
updated_at: TIMESTAMP


────────────────────────────

4.10 lot_varieties（ロット-品種）
lot_id: BIGINT FK → lots(id)
variety_id: BIGINT FK → varieties(id)
ratio_pct: DECIMAL(5,2)
PRIMARY KEY (lot_id, variety_id)


────────────────────────────

4.11 tasting_notes（フレーバーノート）
id: BIGINT PK
category: VARCHAR(50)
name: VARCHAR(100) NOT NULL
created_at: TIMESTAMP
updated_at: TIMESTAMP


────────────────────────────

4.12 lot_tasting_notes（ロット-フレーバーノート）
lot_id: BIGINT FK → lots(id)
tasting_note_id: BIGINT FK → tasting_notes(id)
intensity: SMALLINT CHECK (intensity >= 1 AND intensity <= 5)
PRIMARY KEY(lot_id, tasting_note_id)


────────────────────────────

4.13 certifications（認証）
id: BIGINT PK
code: VARCHAR(20) UNIQUE  // ORG, RA, FT 等
name: VARCHAR(150)
description: TEXT


────────────────────────────

4.14 farm_certifications（農園-認証）
farm_id: BIGINT FK → farms(id)
certification_id: BIGINT FK → certifications(id)
valid_from: DATE
valid_to: DATE
PRIMARY KEY (farm_id, certification_id)


────────────────────────────

4.15 cupping_sessions（カッピングセッション）
id: BIGINT PK
lot_id: BIGINT FK → lots(id)
session_date: DATE NOT NULL
cupper_name: VARCHAR(100)
location: VARCHAR(150)
created_at: TIMESTAMP
updated_at: TIMESTAMP


────────────────────────────

4.16 cupping_scores（カッピングスコア詳細）
id: BIGINT PK
session_id: BIGINT FK → cupping_sessions(id)
aroma: DECIMAL(4,2)
flavor: DECIMAL(4,2)
acidity: DECIMAL(4,2)
body: DECIMAL(4,2)
balance: DECIMAL(4,2)
aftertaste: DECIMAL(4,2)
uniformity: DECIMAL(4,2)
clean_cup: DECIMAL(4,2)
sweetness: DECIMAL(4,2)
total_score: DECIMAL(5,2)

5. REST API エンドポイント仕様（Codex がルーター生成に使える形式）
5.1 基本ルール

ベースURL: /api/v1

全レスポンスは JSON

ページング: ?page=1&per_page=50

ソート: ?sort=created_at&order=desc

5.2 CRUD エンドポイント一覧
GET    /countries
GET    /countries/{id}
POST   /countries
PUT    /countries/{id}
DELETE /countries/{id}

GET    /regions
GET    /regions/{id}
POST   /regions
PUT    /regions/{id}
DELETE /regions/{id}

GET    /subregions
GET    /subregions/{id}
POST   /subregions
PUT    /subregions/{id}
DELETE /subregions/{id}

GET    /farms
GET    /farms/{id}
POST   /farms
PUT    /farms/{id}
DELETE /farms/{id}

GET    /lots
GET    /lots/{id}
POST   /lots
PUT    /lots/{id}
DELETE /lots/{id}

GET    /varieties
GET    /varieties/{id}

GET    /processes
GET    /processes/{id}

GET    /tasting-notes
GET    /tasting-notes/{id}

GET    /cupping-sessions
GET    /cupping-sessions/{id}

6. 検索・フィルタリング仕様（Codex がクエリ実装に使える）
6.1 Farm 検索
GET /farms?country_code=ET&region_id=3&min_altitude=1600&max_altitude=2200&q=gesha


検索条件：

country_code（国コード）

region_id（地域）

subregion_id（サブ地域）

min_altitude / max_altitude

q（フリーワード：農園名、説明）

6.2 Lot 検索
GET /lots?country_code=BR&variety_id=1&harvest_year=2023&min_score=87&tasting=strawberry


検索条件：

country_code

farm_id

variety_id

process_id

harvest_year

min_score / max_score（カッピング）

tasting（フレーバーノート検索）

min_altitude / max_altitude

7. バリデーション要件

記述を省略しないよう明確に指定：

intensity: 1〜5 の整数

moisture_percent: 0〜20

water_activity: 0.40〜0.70

harvest_year: 1900〜2100

ratio_pct: 0〜100

total_score: 0〜100

8. 初期データ（Codex にシード生成させるための指示）

Codex に “生成可能な例” として以下を指定：

国の例：

Ethiopia (ET)
Colombia (CO)
Brazil (BR)
Kenya (KE)
Guatemala (GT)


品種の例：

Gesha, Bourbon, Typica, Caturra, SL28, SL34


精製方法の例：

Washed, Natural, Honey, Anaerobic, Carbonic Maceration


フレーバーノート例：

Strawberry (fruit)
Jasmine (floral)
Black tea (tea_like)
Citrus (fruit)
Chocolate (sweet)

9. 非機能要件（Codex が構成を判断しやすいよう指定）

レスポンスは基本 200、作成は 201 を返す

エラーは JSON で返す

全エンドポイントの型は Pydantic モデルで明示

1リクエストあたり最大 100件まで返す

全ての日時は ISO8601 形式

10. コード生成指示（Codex 用最終命令）

Codex に実装させる際は次の命令を添付すればよい：

以下の完全仕様に基づき、FastAPI + SQLAlchemy + Pydantic で
・データベースモデル（SQLAlchemy）
・Pydantic の Request/Response モデル
・CRUD 全ルート
・高度検索用クエリ
・DB 初期化スクリプト
・初期データ投入スクリプト（seed）
を自動生成してください。
