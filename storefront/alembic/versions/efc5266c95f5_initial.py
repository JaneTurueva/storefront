"""Initial

Revision ID: efc5266c95f5
Revises: 
Create Date: 2019-03-07 17:19:21.408141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efc5266c95f5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'companies',
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('clock_timestamp()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('clock_timestamp()'), nullable=False),
        sa.PrimaryKeyConstraint('company_id', name=op.f('pk__companies'))
    )
    op.create_table(
        'employees',
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('clock_timestamp()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('clock_timestamp()'), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], name=op.f('fk__employees__company_id__companies')),
        sa.PrimaryKeyConstraint('employee_id', name=op.f('pk__employees'))
    )
    op.create_table(
        'products',
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('price', sa.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('clock_timestamp()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('clock_timestamp()'), nullable=False),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.employee_id'], name=op.f('fk__products__employee_id__employees')),
        sa.PrimaryKeyConstraint('product_id', name=op.f('pk__products'))
    )


def downgrade():
    op.drop_table('products')
    op.drop_table('employees')
    op.drop_table('companies')

