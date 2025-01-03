from sqlalchemy.orm import Session

from app.db.models import AppStatus, WorkLocation, WorkType


class TestApplication:
    def test_create(self, session: Session, new_application, new_company, new_user):
        session.add(new_application)
        session.commit()
        session.refresh(new_application)

        assert new_application.role == "test role"
        assert new_application.notes == "test notes"
        assert new_application.application_url == "https://test_url.com"
        assert new_application.status == AppStatus.APPLIED
        assert new_application.work_location == WorkLocation.ON_SITE
        assert new_application.work_type == WorkType.FULL_TIME
        assert new_application.interview_date is None
        assert new_application.user == new_user
        assert new_application.company == new_company
        assert new_application.user_id == new_user.id
        assert new_application.company_id == new_company.id
