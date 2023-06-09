"""Create Note Model

Revision ID: 88353439fac2
Revises: 8b97a0c567f2
Create Date: 2023-06-02 19:55:50.871220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88353439fac2'
down_revision = '8b97a0c567f2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('note',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('author', sa.String(), nullable=False),
    sa.Column('release_year', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='tenant'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('note', schema='tenant')
    # ### end Alembic commands ###
