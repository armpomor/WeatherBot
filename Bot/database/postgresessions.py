from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config.config import DB_HOST, DB_USER, DB_NAME, DB_PASS
# from config.config_dev import DB_HOST, DB_USER, DB_NAME, DB_PASS
from database.models import Base, Person, WeatherHistory


def connect_db():
    # To interact with the database, we create an engine - an object of the Engine class.
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
    # Creating tables
    Base.metadata.create_all(bind=engine)
    return engine


########################### Interaction with the Person table ###################################################
def session_add(person: dict, engine):
    """
    Create a database connection session
    and add a record to the Person table
    """
    with Session(autoflush=True, bind=engine) as db:
        # Create a Person object to add to the database
        user = Person(**person)
        # Adding to the database
        db.add(user)

        db.commit()


def session_number_rows(engine, user_id) -> bool:
    """
    The function determines if there is an entry with the settings of a specific user
    """
    with Session(autoflush=True, bind=engine) as db:
        if len(db.query(Person).filter(Person.user_id == user_id).all()) == 0:
            return False
        return True


def session_update_settings(engine, person: dict, user_id):
    """
    The function updates the user's settings.
    """
    with Session(autoflush=True, bind=engine) as db:
        user = db.query(Person).filter(Person.user_id == user_id).first()
        user.name = person['name']
        user.language = person['language']
        try:
            user.coordinates = person['coordinates']
        except KeyError:
            pass

        db.commit()


def session_get_coordinates(engine, user_id) -> str:
    """
    The function retrieves the coordinates from the user profile
    """
    with Session(autoflush=True, bind=engine) as db:
        user = db.query(Person).filter(Person.user_id == user_id).first()
        return user.coordinates


def session_get_language(engine, user_id) -> str:
    """
    The function retrieves the language from the user profile
    """
    with Session(autoflush=True, bind=engine) as db:
        user = db.query(Person).filter(Person.user_id == user_id).first()
        return user.language


########################### Interaction with the WeatherHistory table ###################################################

def session_add_row(data: dict, engine):
    """
    Create a database connection session
    and add an entry to the WeatherHistory table
    """
    with Session(autoflush=True, bind=engine) as db:
        # Create an object to add to the database
        data = WeatherHistory(**data)
        # Adding to the database
        db.add(data)

        db.commit()


if __name__ == '__main__':
    pass
