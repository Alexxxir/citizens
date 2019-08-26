"""empty message

Revision ID: d7f2b2669b5b
Revises: f21d6297fd7b
Create Date: 2019-08-25 22:19:55.356906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7f2b2669b5b'
down_revision = 'f21d6297fd7b'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(sa.schema.CreateSequence(sa.Sequence('import_id_seq')))


def downgrade():
    pass
