import sys

from database import SessionLocal, engine, verify_database_connection, DatabaseConnectionError
import models


def seed():
    db = SessionLocal()
    try:
        if db.query(models.Country).count() == 0:
            countries = [
                models.Country(code="ET", name_en="Ethiopia"),
                models.Country(code="CO", name_en="Colombia"),
                models.Country(code="BR", name_en="Brazil"),
                models.Country(code="KE", name_en="Kenya"),
                models.Country(code="GT", name_en="Guatemala"),
            ]
            db.add_all(countries)
            db.commit()

        if db.query(models.Variety).count() == 0:
            varieties = [
                models.Variety(name="Gesha"),
                models.Variety(name="Bourbon"),
                models.Variety(name="Typica"),
                models.Variety(name="Caturra"),
                models.Variety(name="SL28"),
                models.Variety(name="SL34"),
            ]
            db.add_all(varieties)
            db.commit()

        if db.query(models.Process).count() == 0:
            processes = [
                models.Process(name="Washed"),
                models.Process(name="Natural"),
                models.Process(name="Honey"),
                models.Process(name="Anaerobic"),
                models.Process(name="Carbonic Maceration"),
            ]
            db.add_all(processes)
            db.commit()

        if db.query(models.TastingNote).count() == 0:
            notes = [
                models.TastingNote(category="fruit", name="Strawberry"),
                models.TastingNote(category="floral", name="Jasmine"),
                models.TastingNote(category="tea_like", name="Black tea"),
                models.TastingNote(category="fruit", name="Citrus"),
                models.TastingNote(category="sweet", name="Chocolate"),
            ]
            db.add_all(notes)
            db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    try:
        verify_database_connection()
    except DatabaseConnectionError as exc:  # pragma: no cover - user guidance only
        print(exc)
        sys.exit(1)

    models.Base.metadata.create_all(bind=engine)
    seed()
