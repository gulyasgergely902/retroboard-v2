# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Database handler"""

import json
from sqlite3 import DatabaseError

from database.models import Setting, Base
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker


class DatabaseHandler:
    """Main class for database handling"""

    def __init__(self, db_url="sqlite:///database/data.sqlite"):
        self.engine = create_engine(db_url, echo=False)
        self.session_local = sessionmaker(bind=self.engine)

        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, _connection_record):
            dbapi_connection.execute("PRAGMA foreign_keys = ON")

    def create_tables(self):
        """Create new database tables"""
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """Get database session"""
        return self.session_local()

    def sync_settings(self, session: Session):
        """Reads settings file and adds not yet existing settings to the DB"""
        with open("settings.json", "r", encoding="utf-8") as settings_file:
            settings_list = json.load(settings_file)

        for setting in settings_list:
            exists = session.query(Setting).filter_by(setting_name=setting["setting_name"]).first()
            if not exists:
                try:
                    tmp_setting = Setting(
                        setting_name=setting["setting_name"],
                        setting_value=setting["default_value"],
                        setting_type=setting["setting_type"],
                        setting_display_name=setting["setting_display_name"],
                        setting_description=setting["setting_description"]
                    )
                    session.add(tmp_setting)
                except DatabaseError:
                    session.rollback()
                    raise

        session.commit()
