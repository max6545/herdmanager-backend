"""add lot&group-history

Revision ID: 3f601e3e59fc
Revises: 2232962d9c61
Create Date: 2023-12-09 12:11:06.193827

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3f601e3e59fc'
down_revision = '2232962d9c61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group_history',
                    sa.Column('changed_at', sa.DateTime(), nullable=True),
                    sa.Column('group_id', sa.String(length=255), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('watermelon_id', sa.String(length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('last_changed_at', sa.DateTime(), nullable=True),
                    sa.Column('farm_id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('group_history_changelog',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('watermelon_id', sa.String(length=255), nullable=True),
                    sa.Column('farm_id', sa.Integer(), nullable=True),
                    sa.Column('action_at', sa.DateTime(), nullable=True),
                    sa.Column('operation', sa.Enum('CREATE', 'UPDATE', 'DELETE', name='changeoperationtype'),
                              nullable=False),
                    sa.Column('old_value', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('group_history_new_members',
                    sa.Column('history_id', sa.String(length=255), nullable=False),
                    sa.Column('animal_id', sa.String(length=255), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('watermelon_id', sa.String(length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('last_changed_at', sa.DateTime(), nullable=True),
                    sa.Column('farm_id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('group_history_new_members_changelog',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('watermelon_id', sa.String(length=255), nullable=True),
                    sa.Column('farm_id', sa.Integer(), nullable=True),
                    sa.Column('action_at', sa.DateTime(), nullable=True),
                    sa.Column('operation', sa.Enum('CREATE', 'UPDATE', 'DELETE', name='changeoperationtype'),
                              nullable=False),
                    sa.Column('old_value', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('group_history_old_members',
                    sa.Column('history_id', sa.String(length=255), nullable=False),
                    sa.Column('animal_id', sa.String(length=255), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('watermelon_id', sa.String(length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('last_changed_at', sa.DateTime(), nullable=True),
                    sa.Column('farm_id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('group_history_old_members_changelog',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('watermelon_id', sa.String(length=255), nullable=True),
                    sa.Column('farm_id', sa.Integer(), nullable=True),
                    sa.Column('action_at', sa.DateTime(), nullable=True),
                    sa.Column('operation', sa.Enum('CREATE', 'UPDATE', 'DELETE', name='changeoperationtype'),
                              nullable=False),
                    sa.Column('old_value', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('lot_history',
                    sa.Column('changed_at', sa.DateTime(), nullable=True),
                    sa.Column('lot_id', sa.String(length=255), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('watermelon_id', sa.String(length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('last_changed_at', sa.DateTime(), nullable=True),
                    sa.Column('farm_id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('lot_history_changelog',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('watermelon_id', sa.String(length=255), nullable=True),
                    sa.Column('farm_id', sa.Integer(), nullable=True),
                    sa.Column('action_at', sa.DateTime(), nullable=True),
                    sa.Column('operation', sa.Enum('CREATE', 'UPDATE', 'DELETE', name='changeoperationtype'),
                              nullable=False),
                    sa.Column('old_value', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('lot_history_new_members',
                    sa.Column('history_id', sa.String(length=255), nullable=False),
                    sa.Column('animal_id', sa.String(length=255), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('watermelon_id', sa.String(length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('last_changed_at', sa.DateTime(), nullable=True),
                    sa.Column('farm_id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('lot_history_new_members_changelog',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('watermelon_id', sa.String(length=255), nullable=True),
                    sa.Column('farm_id', sa.Integer(), nullable=True),
                    sa.Column('action_at', sa.DateTime(), nullable=True),
                    sa.Column('operation', sa.Enum('CREATE', 'UPDATE', 'DELETE', name='changeoperationtype'),
                              nullable=False),
                    sa.Column('old_value', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('lot_history_old_members',
                    sa.Column('history_id', sa.String(length=255), nullable=False),
                    sa.Column('animal_id', sa.String(length=255), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('watermelon_id', sa.String(length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('last_changed_at', sa.DateTime(), nullable=True),
                    sa.Column('farm_id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('lot_history_old_members_changelog',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('watermelon_id', sa.String(length=255), nullable=True),
                    sa.Column('farm_id', sa.Integer(), nullable=True),
                    sa.Column('action_at', sa.DateTime(), nullable=True),
                    sa.Column('operation', sa.Enum('CREATE', 'UPDATE', 'DELETE', name='changeoperationtype'),
                              nullable=False),
                    sa.Column('old_value', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lot_history_old_members_changelog')
    op.drop_table('lot_history_old_members')
    op.drop_table('lot_history_new_members_changelog')
    op.drop_table('lot_history_new_members')
    op.drop_table('lot_history_changelog')
    op.drop_table('lot_history')
    op.drop_table('group_history_old_members_changelog')
    op.drop_table('group_history_old_members')
    op.drop_table('group_history_new_members_changelog')
    op.drop_table('group_history_new_members')
    op.drop_table('group_history_changelog')
    op.drop_table('group_history')
    # ### end Alembic commands ###
