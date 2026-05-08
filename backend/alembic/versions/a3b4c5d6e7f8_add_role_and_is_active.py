"""add role and is_active to users

Revision ID: a3b4c5d6e7f8
Revises: 2a5cb59a134d
Create Date: 2026-05-08 13:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3b4c5d6e7f8'
down_revision: Union[str, None] = '2a5cb59a134d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Thêm cột role (enum: admin, user) với default là 'user'
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.Enum('admin', 'user', name='user_role'),
            nullable=False,
            server_default='user',
        ),
    )

    # Thêm cột is_active (boolean) với default là True
    op.add_column(
        'users',
        sa.Column(
            'is_active',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('1'),
        ),
    )

    # Set admin role cho user đầu tiên (admin@example.com)
    op.execute("UPDATE users SET role = 'admin' WHERE id = 1")


def downgrade() -> None:
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'role')
    # Xóa enum type nếu database hỗ trợ
    op.execute("DROP TYPE IF EXISTS user_role")
