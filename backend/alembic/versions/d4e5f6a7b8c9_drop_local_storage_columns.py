"""Drop legacy columns: file_path, storage_provider, content, page_count

Revision ID: d4e5f6a7b8c9
Revises: c1d2e3f4a5b6
Create Date: 2026-05-16 17:00:00.000000

Changes:
- papers: xóa cột file_path (không còn lưu file local)
- papers: xóa cột storage_provider (chỉ dùng Supabase, không cần phân biệt)
- papers: xóa cột content (text extract chỉ giữ trong RAM, không lưu DB)
- papers: xóa cột page_count (metadata không cần thiết)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import LONGTEXT


# revision identifiers, used by Alembic.
revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, Sequence[str], None] = 'c1d2e3f4a5b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Drop file_path, storage_provider, content, page_count columns."""
    op.drop_column('papers', 'file_path')
    op.drop_column('papers', 'storage_provider')
    op.drop_column('papers', 'content')
    op.drop_column('papers', 'page_count')


def downgrade() -> None:
    """Re-add dropped columns."""
    op.add_column('papers', sa.Column('page_count', sa.Integer(), nullable=True))
    op.add_column('papers', sa.Column('content', LONGTEXT(), nullable=True))
    op.add_column('papers', sa.Column('storage_provider', sa.String(50), nullable=True))
    op.add_column('papers', sa.Column('file_path', sa.String(1024), nullable=True))
