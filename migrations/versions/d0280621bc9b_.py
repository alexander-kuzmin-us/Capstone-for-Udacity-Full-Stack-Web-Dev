"""empty message

Revision ID: d0280621bc9b
Revises: 
Create Date: 2020-03-08 19:09:50.763100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0280621bc9b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('charters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('charters_name', sa.String(), nullable=True),
    sa.Column('departure_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('skippers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('charter_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['charter_id'], ['charters.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('skippers')
    op.drop_table('charters')
    # ### end Alembic commands ###