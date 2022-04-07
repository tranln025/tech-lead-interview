"""Create jumpdrive_device and jumpdrive_event tables with OBD data for associated vins
Revision ID: 2a3a43a739b2
Revises: 989c42061f8c
Create Date: 2022-04-04 10:26:58.712630
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2a3a43a739b2"
down_revision = "989c42061f8c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "jumpdrive_device",
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("jumpdrive_device_id", sa.BigInteger(), nullable=False),
        sa.Column("serial_number", sa.String(length=63), nullable=False),
        sa.Column("vin", sa.String(length=63), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("jumpdrive_device_id"),
    )
    op.create_table(
        "jumpdrive_event",
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("jumpdrive_event_id", sa.BigInteger(), nullable=False),
        sa.Column("serial_number", sa.String(length=63), nullable=False),
        sa.Column("vin", sa.String(length=63), nullable=False),
        sa.Column("last_time_in", sa.Integer(), nullable=False),
        sa.Column("fuel_percent", sa.Float(), nullable=True),
        sa.Column("battery_level_mV", sa.Integer(), nullable=True),
        sa.Column("odometer_km", sa.Float(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("jumpdrive_event_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("jumpdrive_event")
    op.drop_table("jumpdrive_device")
    # ### end Alembic commands ###