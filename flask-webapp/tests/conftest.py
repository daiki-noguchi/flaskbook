from pathlib import Path
import shutil
import pytest
from flask_webapp.app import create_app, db
from flask_webapp.crud.models import User
from flask_webapp.detector.models import UserImage, UserImageTag


@pytest.fixture
def app_data() -> int:
    return 3


@pytest.fixture
def fixture_app():
    app = create_app("testing")
    app.app_context().push()
    with app.app_context():
        db.create_all()
    test_images_dir_path = Path(app.config["UPLOAD_FOLDER"])
    test_images_dir_path.mkdir(exist_ok=True, parents=True)
    yield app
    User.query.delete()
    UserImage.query.delete()
    UserImageTag.query.delete()
    shutil.rmtree(test_images_dir_path)
    db.session.commit()


@pytest.fixture
def client(fixture_app):
    return fixture_app.test_client()
