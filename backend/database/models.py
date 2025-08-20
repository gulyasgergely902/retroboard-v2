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

"""Database models"""

from typing import List

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database_handler import Base


class Board(Base):
    """Database model of a Board object"""

    __tablename__ = "boards"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    notes: Mapped[List["Note"]] = relationship(
        back_populates="board", cascade="all, delete-orphan"
    )
    categories: Mapped[List["Category"]] = relationship(
        back_populates="board", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Board(id={self.id!r}, name={self.name!r},notes={self.notes!r})"


class Note(Base):
    """Database model of a Note"""

    __tablename__ = "notes"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(30))
    category: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    tags: Mapped[list] = mapped_column(JSON)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id"))

    board: Mapped["Board"] = relationship(back_populates="notes")

    def __repr__(self) -> str:
        return (
            f"Note(id={self.id!r}, description={self.description!r},"
            f"category={self.category!r}, tags={self.tags!r})"
        )


class Category(Base):
    """Database model of Category"""

    __tablename__ = "categories"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id"))

    board: Mapped["Board"] = relationship(back_populates="categories")

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r})"
