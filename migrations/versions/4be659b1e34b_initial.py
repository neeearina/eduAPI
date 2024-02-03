"""initial

Revision ID: 4be659b1e34b
Revises: 
Create Date: 2024-02-01 19:58:31.078681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '4be659b1e34b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cities',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('tags',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('organizations',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('director', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=True),
                    sa.Column('site', sa.String(), nullable=True),
                    sa.Column('address', sa.String(), nullable=True),
                    sa.Column('city_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('name'),
                    sa.UniqueConstraint('site')
                    )
    op.create_table('clubs',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('organization_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('clubs_tags',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('club_id', sa.Integer(), nullable=True),
                    sa.Column('tag_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['club_id'], ['clubs.id'], ),
                    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clubs_tags')
    op.drop_table('clubs')
    op.drop_table('organizations')
    op.drop_table('tags')
    op.drop_table('cities')
    # ### end Alembic commands ###