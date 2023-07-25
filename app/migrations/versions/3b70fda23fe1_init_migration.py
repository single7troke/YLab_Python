"""init_migration

Revision ID: 3b70fda23fe1
Revises: 
Create Date: 2023-07-25 07:02:22.757913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b70fda23fe1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('submenu_counter', sa.SmallInteger(), nullable=False),
    sa.Column('dish_counter', sa.SmallInteger(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('submenu',
    sa.Column('dish_counter', sa.SmallInteger(), nullable=False),
    sa.Column('menu_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('dish',
    sa.Column('price', sa.String(), nullable=False),
    sa.Column('submenu_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['submenu_id'], ['submenu.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dish')
    op.drop_table('submenu')
    op.drop_table('menu')
    # ### end Alembic commands ###
