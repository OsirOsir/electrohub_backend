"""changed reviews

Revision ID: 032e833e964d
Revises: bb6c1ba17de0
Create Date: 2024-11-13 14:40:32.678315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '032e833e964d'
down_revision = 'bb6c1ba17de0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.drop_constraint('fk_reviews_item_id_items', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_reviews_item_id_items'), 'items', ['item_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_reviews_item_id_items'), type_='foreignkey')
        batch_op.create_foreign_key('fk_reviews_item_id_items', 'items', ['item_id'], ['id'])

    # ### end Alembic commands ###