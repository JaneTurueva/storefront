"""Unique company name

Revision ID: f208299fca48
Revises: efc5266c95f5
Create Date: 2019-03-07 17:51:34.619595

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'f208299fca48'
down_revision = 'efc5266c95f5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(op.f('uq__companies__name'), 'companies',
                                ['name'])


def downgrade():
    op.drop_constraint(op.f('uq__companies__name'), 'companies',
                       type_='unique')
