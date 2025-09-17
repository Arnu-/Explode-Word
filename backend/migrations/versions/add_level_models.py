"""添加关卡和游戏记录模型

Revision ID: add_level_models
Revises: 
Create Date: 2025-09-17 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_level_models'
down_revision = None
depends_on = None


def upgrade():
    # 创建关卡表
    op.create_table('levels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('difficulty', sa.String(length=20), nullable=False),
        sa.Column('estimated_time_minutes', sa.Integer(), nullable=True),
        sa.Column('max_score', sa.Integer(), nullable=True),
        sa.Column('tasks_config', sa.Text(), nullable=True),
        sa.Column('unlock_level_id', sa.Integer(), nullable=True),
        sa.Column('unlock_stars_required', sa.Integer(), nullable=True),
        sa.Column('reward_coins', sa.Integer(), nullable=True),
        sa.Column('reward_exp', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['unlock_level_id'], ['levels.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建用户关卡记录表
    op.create_table('level_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('level_id', sa.Integer(), nullable=False),
        sa.Column('best_score', sa.Integer(), nullable=True),
        sa.Column('total_attempts', sa.Integer(), nullable=True),
        sa.Column('completed_attempts', sa.Integer(), nullable=True),
        sa.Column('stars', sa.Integer(), nullable=True),
        sa.Column('tasks_completion', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('best_time_seconds', sa.Integer(), nullable=True),
        sa.Column('total_time_seconds', sa.Integer(), nullable=True),
        sa.Column('last_played_at', sa.DateTime(), nullable=True),
        sa.Column('first_completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['level_id'], ['levels.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'level_id', name='unique_user_level')
    )
    
    # 创建游戏历史记录表
    op.create_table('game_histories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('level_id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('time_seconds', sa.Integer(), nullable=True),
        sa.Column('stars_earned', sa.Integer(), nullable=True),
        sa.Column('correct_answers', sa.Integer(), nullable=True),
        sa.Column('wrong_answers', sa.Integer(), nullable=True),
        sa.Column('total_questions', sa.Integer(), nullable=True),
        sa.Column('tasks_result', sa.Text(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=True),
        sa.Column('is_new_record', sa.Boolean(), nullable=True),
        sa.Column('played_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['level_id'], ['levels.id'], ),
        sa.ForeignKeyConstraint(['session_id'], ['game_sessions.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('game_histories')
    op.drop_table('level_records')
    op.drop_table('levels')