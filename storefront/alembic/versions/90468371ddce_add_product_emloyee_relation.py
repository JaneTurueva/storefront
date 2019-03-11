"""Add product emloyee relation

Revision ID: 90468371ddce
Revises: f208299fca48
Create Date: 2019-03-11 18:53:38.402117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90468371ddce'
down_revision = 'f208299fca48'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'employee_product_relations',
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['employee_id'], ['employees.employee_id'],
            name=op.f('fk__employee_product_relations__employee_id__employees')
        ),
        sa.ForeignKeyConstraint(
            ['product_id'], ['products.product_id'],
            name=op.f('fk__employee_product_relations__product_id__products')
        ),
        sa.PrimaryKeyConstraint('employee_id', 'product_id',
                                name=op.f('pk__employee_product_relations'))
    )

    op.drop_constraint('fk__products__employee_id__employees', 'products',
                       type_='foreignkey')
    op.drop_column('products', 'employee_id')


def downgrade():
    op.add_column('products', sa.Column('employee_id', sa.INTEGER(),
                                        autoincrement=False, nullable=False))
    op.create_foreign_key(
        'fk__products__employee_id__employees', 'products', 'employees',
        ['employee_id'], ['employee_id']
    )
    op.drop_table('employee_product_relations')
