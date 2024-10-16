"""added username

Revision ID: 0656a8db9b30
Revises: ec085e451bdf
Create Date: 2024-10-11 08:26:22.274731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0656a8db9b30'
down_revision = 'ec085e451bdf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=20), nullable=False))
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('username')

    # ### end Alembic commands ###
