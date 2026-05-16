"""Drop legacy columns: file_path, storage_provider, content, page_count

Revision ID: d4e5f6a7b8c9
Revises: c1d2e3f4a5b6
Create Date: 2026-05-16 17:00:00.000000

Changes:
- papers: xóa cột file_path (nếu tồn tại)
- papers: xóa cột storage_provider (nếu tồn tại)
- papers: xóa cột content (text extract không cần lưu DB)
- papers: xóa cột page_count (metadata không cần thiết)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect
from sqlalchemy.dialects.mysql import LONGTEXT


# revision identifiers, used by Alembic.
revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, Sequence[str], None] = 'c1d2e3f4a5b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(table_name: str, column_name: str) -> bool:
    """Kiểm tra cột có tồn tại trong bảng không."""
    bind = op.get_bind()
    insp = inspect(bind)
    columns = [col["name"] for col in insp.get_columns(table_name)]
    return column_name in columns


def upgrade() -> None:
    """Drop legacy columns (chỉ xóa nếu cột tồn tại)."""
    for col in ["file_path", "storage_provider", "content", "page_count"]:
        if _column_exists("papers", col):
            op.drop_column("papers", col)


def downgrade() -> None:
    """Re-add dropped columns."""
    if not _column_exists("papers", "page_count"):
        op.add_column('papers', sa.Column('page_count', sa.Integer(), nullable=True))
    if not _column_exists("papers", "content"):
        op.add_column('papers', sa.Column('content', LONGTEXT(), nullable=True))
    if not _column_exists("papers", "storage_provider"):
        op.add_column('papers', sa.Column('storage_provider', sa.String(50), nullable=True))
    if not _column_exists("papers", "file_path"):
        op.add_column('papers', sa.Column('file_path', sa.String(1024), nullable=True))
