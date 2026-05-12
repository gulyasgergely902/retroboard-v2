"""
Add CASCADE delete to notes board_id foreign key

Revision ID: 001
Revises:
Create Date: 2026-05-12

"""
from alembic import op


revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade: add CASCADE delete to notes board_id foreign key"""
    with op.batch_alter_table('notes', schema=None) as batch_op:
        batch_op.drop_constraint('fk_notes_board_id', type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_notes_board_id',
            'boards',
            ['board_id'],
            ['id'],
            ondelete='CASCADE'
        )


def downgrade() -> None:
    """Downgrade: remove CASCADE delete from notes board_id foreign key"""
    with op.batch_alter_table('notes', schema=None) as batch_op:
        batch_op.drop_constraint('fk_notes_board_id', type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_notes_board_id',
            'boards',
            ['board_id'],
            ['id']
        )
