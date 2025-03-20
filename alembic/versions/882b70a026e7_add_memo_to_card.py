"""Add memo to card

Revision ID: 882b70a026e7
Revises: 2b8b8bdba788
Create Date: 2025-03-20 12:20:22.102787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '882b70a026e7'
down_revision: Union[str, None] = '2b8b8bdba788'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('memo', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('card', 'memo')
    # ### end Alembic commands ###
