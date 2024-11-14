"""Remove test column

Revision ID: bb6c1ba17de0
Revises: a93ac17f9556
Create Date: 2024-11-13 14:30:57.431362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb6c1ba17de0'
down_revision = 'a93ac17f9556'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('test_column')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test_column', sa.VARCHAR(length=80), autoincrement=False, nullable=True))

    # ### end Alembic commands ###