from alembic import op
import sqlalchemy as sa

revision = "8fc41f03b551"
down_revision = "88f79ce9da68"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "task_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "task_id",
            sa.Integer,
            sa.ForeignKey("tasks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("message", sa.String, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime,
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_table("task_logs")
