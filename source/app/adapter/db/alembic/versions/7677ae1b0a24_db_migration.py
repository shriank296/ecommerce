"""DB migration

Revision ID: 7677ae1b0a24
Revises: 566742e54f4e
Create Date: 2025-02-18 04:14:10.208046

"""

import csv
import uuid
from pathlib import Path
from typing import Sequence, Union

from alembic import op
from sqlalchemy.orm import Session, declarative_base

from source.app.adapter.db.model.category import Category

Base = declarative_base()

# revision identifiers, used by Alembic.
revision: str = "7677ae1b0a24"
down_revision: Union[str, None] = "566742e54f4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    session = Session(bind=op.get_bind())

    BASE_DIR = Path(__file__).resolve().parents[1]  # Go up two levels
    categories_file_path = f"{BASE_DIR}/csv/categories.csv"

    name_map = {}

    with open(categories_file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name_map[row["name"]] = uuid.uuid4()

            category = Category(
                id=name_map[row["name"]], name=row["name"], parent_category_id=None
            )

            session.add(category)
        session.commit()

    with open(categories_file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["parent"]:
                category = (
                    session.query(Category).filter_by(id=name_map[row["name"]]).first()
                )
                category.parent_category_id = name_map[row["parent"]]
        session.commit()
    session.close()

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
