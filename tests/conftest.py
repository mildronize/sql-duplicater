import pytest

from sql_duplicater import create_app
from sql_duplicater.models import db, User


@pytest.fixture()
def testapp(request):
    app = create_app('sql_duplicater.settings.TestConfig')
    client = app.test_client()

    db.app = app
    db.create_all()

    if getattr(request.module, "create_user", True):
        admin = User('admin', 'supersafepassword')
        db.session.add(admin)
        db.session.commit()

    def teardown():
        db.session.remove()
        db.drop_all()

    request.addfinalizer(teardown)

    return client
