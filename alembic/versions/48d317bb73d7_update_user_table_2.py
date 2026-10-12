"""update user table 2

Revision ID: 48d317bb73d7
Revises: c68b5ae57012
Create Date: 2026-10-09 23:50:20.176997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48d317bb73d7'
down_revision: Union[str, Sequence[str], None] = 'c68b5ae57012'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    user_role_enum = sa.Enum('admin', 'manager', 'owner', 'customer', name='userrole')
    user_role_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('users', sa.Column('role', user_role_enum, server_default='customer', nullable=False))    
    op.add_column('users', sa.Column('is_email_verified', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('users', sa.Column('is_phone_verified', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('users', sa.Column('default_delivery_address', sa.String(length=500), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'default_delivery_address')
    op.drop_column('users', 'is_phone_verified')
    op.drop_column('users', 'is_email_verified')
    op.drop_column('users', 'role')
    user_role_enum = sa.Enum('admin', 'manager', 'owner', 'customer', name='userrole')
    user_role_enum.drop(op.get_bind(), checkfirst=True)
