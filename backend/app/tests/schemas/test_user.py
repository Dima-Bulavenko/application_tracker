import pytest
from pydantic import ValidationError

from app.schemas import (
    UserCreate,
    UserRead,
    UserUpdate,
    UserUpdateEmail,
    UserUpdatePassword,
)

# TODO: Refactor: replace schema class names in test functions with class attribute schema_class


class TestUserRead:
    def test_user_read_creation(self, user_data: dict):
        schema = UserRead(**user_data)

        assert schema.id == user_data["id"]
        assert schema.email == user_data["email"]
        assert schema.first_name == user_data["first_name"]
        assert schema.second_name == user_data["second_name"]
        assert schema.time_create == user_data["time_create"]
        assert schema.time_update == user_data["time_update"]
        assert schema.is_active == user_data["is_active"]

    def test_invalid_email(self, user_data: dict):
        user_data["email"] = "invalid_email"

        with pytest.raises(ValidationError) as error_info:
            UserRead(**user_data)

        errors_list = error_info.value.errors()
        error = errors_list[0]

        assert len(errors_list) == 1
        assert error["type"] == "value_error"
        assert error["input"] == "invalid_email"

    def test_first_name_max_length(self, user_data: dict):
        max_length = 40
        user_data["first_name"] = "t" * (max_length + 1)

        with pytest.raises(ValidationError) as error_info:
            UserRead(**user_data)

        errors_list = error_info.value.errors()
        error = errors_list[0]

        assert len(errors_list) == 1
        assert error["type"] == "string_too_long"

    def test_second_name_max_length(self, user_data: dict):
        max_length = 40
        user_data["second_name"] = "t" * (max_length + 1)

        with pytest.raises(ValidationError) as error_info:
            UserRead(**user_data)

        errors_list = error_info.value.errors()
        error = errors_list[0]

        assert len(errors_list) == 1
        assert error["type"] == "string_too_long"

    def test_first_name_default_none(self, user_data: dict):
        user_data.pop("first_name")
        schema = UserRead(**user_data)

        assert schema.first_name is None

    def test_second_name_default_none(self, user_data: dict):
        user_data.pop("second_name")
        schema = UserRead(**user_data)

        assert schema.second_name is None

    def test_time_create_not_datetime_format(self, user_data: dict):
        user_data["time_create"] = "not_time"

        with pytest.raises(ValidationError) as error_info:
            UserRead(**user_data)

        errors_list = error_info.value.errors()
        error = errors_list[0]

        assert len(errors_list) == 1
        assert error["type"] == "datetime_from_date_parsing"
        assert error["input"] == "not_time"

    def test_time_update_not_datetime_format(self, user_data: dict):
        user_data["time_update"] = "not_time"

        with pytest.raises(ValidationError) as error_info:
            UserRead(**user_data)

        errors_list = error_info.value.errors()
        error = errors_list[0]

        assert len(errors_list) == 1
        assert error["type"] == "datetime_from_date_parsing"
        assert error["input"] == "not_time"

    def test_is_active_default_true(self, user_data: dict):
        user_data.pop("is_active")

        schema = UserRead(**user_data)

        assert schema.is_active is True

    def test_email_is_not_optional(self, user_data: dict):
        user_data.pop("email")

        with pytest.raises(ValidationError) as error_info:
            UserRead(**user_data)

        errors_list = error_info.value.errors()
        error = errors_list[0]

        assert len(errors_list) == 1
        assert error["type"] == "missing"
        assert error["msg"] == "Field required"


class TestUserCreate:
    def test_user_create_creation(self, user_data: dict):
        schema = UserCreate(**user_data)

        assert schema.email == user_data["email"]
        assert schema.password.get_secret_value() == user_data["password"]

    def test_invalid_email(self, user_data: dict):
        user_data["email"] = "invalid_email"

        with pytest.raises(ValidationError) as error_info:
            UserCreate(**user_data)

        errors_list = error_info.value.errors()
        error = errors_list[0]

        assert len(errors_list) == 1
        assert error["type"] == "value_error"
        assert error["input"] == "invalid_email"

    def test_email_is_not_optional(self, user_data):
        user_data.pop("email")

        with pytest.raises(ValidationError) as error_info:
            UserCreate(**user_data)

        errors_list = error_info.value.errors()
        error = errors_list[0]

        assert len(errors_list) == 1
        assert error["type"] == "missing"
        assert error["msg"] == "Field required"

    def test_password_is_not_optional(self, user_data):
        user_data.pop("password")

        with pytest.raises(ValidationError) as error_info:
            UserCreate(**user_data)

        errors_list = error_info.value.errors()
        error = errors_list[0]

        assert len(errors_list) == 1
        assert error["type"] == "missing"
        assert error["msg"] == "Field required"


class TestUserUpdate:
    def test_creation(self, user_data: dict):
        schema = UserUpdate(**user_data)

        assert schema.first_name == user_data["first_name"]
        assert schema.second_name == user_data["second_name"]
        assert schema.is_active == user_data["is_active"]

    def test_first_name_max_length(self, user_data: dict):
        max_length = 40
        user_data["first_name"] = "t" * (max_length + 1)

        with pytest.raises(ValidationError) as error_info:
            UserUpdate(**user_data)

        errors_list = error_info.value.errors()
        error = errors_list[0]

        assert len(errors_list) == 1
        assert error["type"] == "string_too_long"

    def test_second_name_max_length(self, user_data: dict):
        max_length = 40
        user_data["second_name"] = "t" * (max_length + 1)

        with pytest.raises(ValidationError) as error_info:
            UserUpdate(**user_data)

        errors_list = error_info.value.errors()
        error = errors_list[0]

        assert len(errors_list) == 1
        assert error["type"] == "string_too_long"

    def test_first_name_default_none(self, user_data: dict):
        user_data.pop("first_name")
        schema = UserUpdate(**user_data)

        assert schema.first_name is None

    def test_second_name_default_none(self, user_data: dict):
        user_data.pop("second_name")
        schema = UserUpdate(**user_data)

        assert schema.second_name is None


class TestUserUpdatePassword:
    def test_creation(self, user_data: dict):
        schema = UserUpdatePassword(**user_data)

        assert schema.password.get_secret_value() == user_data["password"]

    def test_password_is_not_optional(self, user_data):
        user_data.pop("password")

        with pytest.raises(ValidationError) as error_info:
            UserUpdatePassword(**user_data)

        errors_list = error_info.value.errors()
        error = errors_list[0]

        assert len(errors_list) == 1
        assert error["type"] == "missing"
        assert error["msg"] == "Field required"


class TestUserUpdateEmail:
    def test_creation(self, user_data: dict):
        schema = UserUpdateEmail(**user_data)

        assert schema.email == user_data["email"]

    def test_email_is_not_optional(self, user_data):
        user_data.pop("email")

        with pytest.raises(ValidationError) as error_info:
            UserUpdateEmail(**user_data)

        errors_list = error_info.value.errors()
        error = errors_list[0]

        assert len(errors_list) == 1
        assert error["type"] == "missing"
        assert error["msg"] == "Field required"


# TODO: Add tests for UserReadRel
