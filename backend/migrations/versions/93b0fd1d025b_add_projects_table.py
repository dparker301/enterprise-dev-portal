"""add projects table ownership fields

Revision ID: 93b0fd1d025b
Revises: 9cfe91c71250
Create Date: 2026-07-17

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "93b0fd1d025b"
down_revision: Union[str, None] = "9cfe91c71250"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add owner_id as nullable first because projects may already exist.
    op.add_column(
        "projects",
        sa.Column(
            "owner_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "projects",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    op.add_column(
        "projects",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    # Prevent the description NOT NULL conversion from failing.
    op.execute(
        """
        UPDATE projects
        SET description = ''
        WHERE description IS NULL
        """
    )

    # Assign existing projects to the first existing user.
    op.execute(
        """
        UPDATE projects
        SET owner_id = (
            SELECT id
            FROM users
            ORDER BY id
            LIMIT 1
        )
        WHERE owner_id IS NULL
        """
    )

    # owner_id can become NOT NULL after existing records are populated.
    op.alter_column(
        "projects",
        "owner_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.alter_column(
        "projects",
        "description",
        existing_type=sa.Text(),
        type_=sa.String(length=500),
        nullable=False,
    )

    op.alter_column(
        "projects",
        "status",
        existing_type=sa.String(length=50),
        type_=sa.String(length=25),
        existing_nullable=True,
        nullable=False,
        server_default="New",
    )

    op.create_foreign_key(
        "fk_projects_owner_id_users",
        "projects",
        "users",
        ["owner_id"],
        ["id"],
    )

    op.drop_column(
        "projects",
        "owner",
    )


def downgrade() -> None:
    op.add_column(
        "projects",
        sa.Column(
            "owner",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.drop_constraint(
        "fk_projects_owner_id_users",
        "projects",
        type_="foreignkey",
    )

    op.alter_column(
        "projects",
        "status",
        existing_type=sa.String(length=25),
        type_=sa.String(length=50),
        existing_nullable=False,
        nullable=True,
        server_default=None,
    )

    op.alter_column(
        "projects",
        "description",
        existing_type=sa.String(length=500),
        type_=sa.Text(),
        existing_nullable=False,
        nullable=True,
    )

    op.drop_column("projects", "updated_at")
    op.drop_column("projects", "created_at")
    op.drop_column("projects", "owner_id")
