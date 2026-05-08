"""add_root_role

Revision ID: 4e5a4d9d2870
Revises: a3b4c5d6e7f8
Create Date: 2026-05-08 16:11:38.953734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e5a4d9d2870'
down_revision: Union[str, Sequence[str], None] = 'a3b4c5d6e7f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Thay đổi kiểu ENUM để hỗ trợ 'root'
    op.execute("ALTER TABLE users MODIFY COLUMN role ENUM('root', 'admin', 'user') NOT NULL DEFAULT 'user'")
    # Nâng cấp tài khoản admin đầu tiên (id=1) lên root
    op.execute("UPDATE users SET role='root' WHERE id=1")


def downgrade() -> None:
    """Downgrade schema."""
    # Đưa tất cả root trở về admin trước khi hạ cấp cột
    op.execute("UPDATE users SET role='admin' WHERE role='root'")
    # Hạ cấp kiểu ENUM
    op.execute("ALTER TABLE users MODIFY COLUMN role ENUM('admin', 'user') NOT NULL DEFAULT 'user'")
