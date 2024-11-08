"""Change hashed_password to password

Revision ID: c399e16a4e5a
Revises: 802824f1b02a
Create Date: 2024-11-04 19:10:39.057428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c399e16a4e5a'
down_revision: Union[str, None] = '802824f1b02a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.String(), nullable=False))
    op.drop_column('user', 'hashed_password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###
