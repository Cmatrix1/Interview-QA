"""Create tags_association_table and references_association_table

Revision ID: a1cd201b6903
Revises: 45c58cd3fe91
Create Date: 2024-02-29 14:28:16.315706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1cd201b6903'
down_revision: Union[str, None] = '45c58cd3fe91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "tags_association_table",
        sa.Column("tag_id", sa.Integer, sa.ForeignKey("tags.id")),
        sa.Column("question_id", sa.Integer, sa.ForeignKey("questions.id")),
    )

    op.create_table(
        "references_association_table",
        sa.Column("reference_id", sa.Integer, sa.ForeignKey("references.id")),
        sa.Column("question_id", sa.Integer, sa.ForeignKey("questions.id")),
    )

def downgrade():
    op.drop_table("tags_association_table")
    op.drop_table("references_association_table")