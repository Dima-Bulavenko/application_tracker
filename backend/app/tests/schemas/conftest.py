from datetime import datetime

import pytest


@pytest.fixture
def user_data():
    return {
        "id": 0,
        "email": "test@gmail.com",
        "first_name": "test_first_name",
        "second_name": "test_second_name",
        "time_create": datetime.now(),
        "time_update": datetime.now(),
        "is_active": True,
        "password": "test_password",
    }
