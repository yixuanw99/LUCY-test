"""index and unique sample_id in Report

Revision ID: 4b4d5180352c
Revises: 996e4e0fd205
Create Date: 2024-09-13 18:20:36.649463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b4d5180352c'
down_revision: Union[str, None] = '996e4e0fd205'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_reports_sample_id'), 'reports', ['sample_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reports_sample_id'), table_name='reports')
    # ### end Alembic commands ###
