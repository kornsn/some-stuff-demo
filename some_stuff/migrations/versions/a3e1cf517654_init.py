"""Init

Revision ID: a3e1cf517654
Revises: 
Create Date: 2020-03-08 05:01:50.400878

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a3e1cf517654'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "some_stuff",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String),
    )


def downgrade():
    op.drop_table("some_stuff")
