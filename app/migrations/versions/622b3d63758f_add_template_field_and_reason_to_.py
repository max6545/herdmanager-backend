"""add template field and reason to treatment

Revision ID: 622b3d63758f
Revises: 3f601e3e59fc
Create Date: 2023-12-14 14:25:12.837663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '622b3d63758f'
down_revision = '3f601e3e59fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('treatment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reason', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('is_template', sa.Boolean(), server_default='0', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('treatment', schema=None) as batch_op:
        batch_op.drop_column('is_template')
        batch_op.drop_column('reason')

    # ### end Alembic commands ###
