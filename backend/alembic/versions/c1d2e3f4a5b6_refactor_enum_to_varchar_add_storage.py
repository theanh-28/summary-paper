"""Refactor: ENUM to VARCHAR, add Object Storage fields, add indexes

Revision ID: c1d2e3f4a5b6
Revises: 42d0ab46bb58
Create Date: 2026-05-16 02:00:00.000000

Changes:
- papers.status: ENUM → VARCHAR(50) (tránh table lock khi ALTER)
- users.role: ENUM → VARCHAR(50) (tránh table lock khi ALTER)
- papers: thêm file_url, storage_path, storage_provider (Object Storage)
- Thêm indexes: idx_papers_status, idx_papers_created_at
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1d2e3f4a5b6'
down_revision: Union[str, Sequence[str], None] = '42d0ab46bb58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # --- 1. papers.status: ENUM → VARCHAR(50) ---
    op.alter_column(
        'papers', 'status',
        existing_type=sa.Enum('uploaded', 'processing', 'completed', 'failed', name='paper_status'),
        type_=sa.String(50),
        existing_nullable=False,
        existing_server_default='uploaded',
    )

    # --- 2. users.role: ENUM → VARCHAR(50) ---
    op.alter_column(
        'users', 'role',
        existing_type=sa.Enum('root', 'admin', 'user', name='user_role'),
        type_=sa.String(50),
        existing_nullable=False,
        existing_server_default='user',
    )

    # --- 3. Thêm cột Object Storage ---
    op.add_column('papers', sa.Column('file_url', sa.String(2048), nullable=True))
    op.add_column('papers', sa.Column('storage_path', sa.String(1024), nullable=True))
    op.add_column('papers', sa.Column('storage_provider', sa.String(50), nullable=True))

    # --- 4. Thêm indexes cho performance ---
    op.create_index('idx_papers_status', 'papers', ['status'])
    op.create_index('idx_papers_created_at', 'papers', ['created_at'])


def downgrade() -> None:
    """Downgrade schema."""

    # Drop indexes
    op.drop_index('idx_papers_created_at', table_name='papers')
    op.drop_index('idx_papers_status', table_name='papers')

    # Drop Object Storage columns
    op.drop_column('papers', 'storage_provider')
    op.drop_column('papers', 'storage_path')
    op.drop_column('papers', 'file_url')

    # Revert VARCHAR → ENUM
    op.alter_column(
        'users', 'role',
        existing_type=sa.String(50),
        type_=sa.Enum('root', 'admin', 'user', name='user_role'),
        existing_nullable=False,
        existing_server_default='user',
    )

    op.alter_column(
        'papers', 'status',
        existing_type=sa.String(50),
        type_=sa.Enum('uploaded', 'processing', 'completed', 'failed', name='paper_status'),
        existing_nullable=False,
        existing_server_default='uploaded',
    )
