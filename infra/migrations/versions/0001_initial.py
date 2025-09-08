from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('agents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('provider', sa.String),
        sa.Column('name', sa.String),
        sa.Column('last_refreshed', sa.DateTime))
    op.create_table('workflows',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('status', sa.String),
        sa.Column('created_at', sa.DateTime))
    op.create_table('approvals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('workflow_id', sa.Integer, sa.ForeignKey('workflows.id')),
        sa.Column('status', sa.String),
        sa.Column('reason', sa.String))
    op.create_table('costs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('workflow_id', sa.Integer, sa.ForeignKey('workflows.id')),
        sa.Column('step', sa.String),
        sa.Column('cost', sa.Float))


def downgrade():
    op.drop_table('costs')
    op.drop_table('approvals')
    op.drop_table('workflows')
    op.drop_table('agents')
