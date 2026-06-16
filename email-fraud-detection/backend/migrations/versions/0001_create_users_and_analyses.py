from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depend_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=320), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=128), nullable=True),
        sa.Column('role', sa.Enum('admin', 'analyst', 'user', name='userrole'), nullable=False, server_default='user'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        'analyses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('email_subject', sa.String(length=255), nullable=True),
        sa.Column('email_from', sa.String(length=320), nullable=True),
        sa.Column('email_to', sa.String(length=1024), nullable=True),
        sa.Column('fraud_score', sa.Integer(), nullable=False),
        sa.Column('labels', sa.JSON(), nullable=False),
        sa.Column('details', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_table('analyses')
    op.drop_table('users')
