"""initialize

Revision ID: 4156b444d614
Revises: 
Create Date: 2025-03-30 23:12:05.070597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4156b444d614'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('registration_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=120), nullable=False),
    sa.Column('used', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('password_hash', sa.String(length=512), nullable=False),
    sa.Column('user_folder', sa.String(length=120), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('registration_code', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('registration_code'),
    sa.UniqueConstraint('user_folder')
    )
    op.create_table('session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('session_name', sa.String(length=120), nullable=False),
    sa.Column('filename', sa.String(length=120), nullable=False),
    sa.Column('created_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('modified_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('session_folder', sa.String(length=120), nullable=False),
    sa.Column('total_page', sa.Integer(), nullable=False),
    sa.Column('config', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('session_folder')
    )
    op.create_table('page',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('page_number', sa.Integer(), nullable=False),
    sa.Column('page_folder', sa.String(length=120), nullable=False),
    sa.Column('tasks', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('page_folder')
    )
    op.create_table('user_session',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=120), nullable=False),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'session_id')
    )
    op.create_table('activity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.Column('page_id', sa.Integer(), nullable=True),
    sa.Column('app', sa.String(length=120), nullable=True),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('type', sa.String(length=120), nullable=False),
    sa.ForeignKeyConstraint(['page_id'], ['page.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('activity')
    op.drop_table('user_session')
    op.drop_table('page')
    op.drop_table('session')
    op.drop_table('user')
    op.drop_table('registration_code')
    # ### end Alembic commands ###
