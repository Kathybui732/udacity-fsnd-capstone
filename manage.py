from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import create_app, db
from api.database.models import User, City, RoadTrip
from tests import db_drop_everything

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

# manage migrations
manager.add_command('db', MigrateCommand)


@manager.command
def routes():
    print(app.url_map)


@manager.command
def db_setup():
    db_drop_everything(db)
    db.create_all()


@manager.command
def db_seed():
    db_drop_everything(db)
    db.create_all()
    # seed anything here we might need to deploy
    db.session.commit()
    # print(f'obj count: {len(db.session.query(Drink).all())}')


if __name__ == "__main__":
    manager.run()
