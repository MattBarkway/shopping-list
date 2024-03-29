"""add indexes

Revision ID: 353ac7208a4e
Revises: 5e0e2dbc5470
Create Date: 2024-02-12 12:12:09.621971

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "353ac7208a4e"
down_revision = "5e0e2dbc5470"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(
        op.f("ix_collaborator_list_id"), "collaborator", ["list_id"], unique=False
    )
    op.create_index(
        op.f("ix_collaborator_user_id"), "collaborator", ["user_id"], unique=False
    )
    op.create_index(op.f("ix_item_sl_id"), "item", ["sl_id"], unique=False)
    op.create_index(
        op.f("ix_shopping_list_user_id"), "shopping_list", ["user_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_shopping_list_user_id"), table_name="shopping_list")
    op.drop_index(op.f("ix_item_sl_id"), table_name="item")
    op.drop_index(op.f("ix_collaborator_user_id"), table_name="collaborator")
    op.drop_index(op.f("ix_collaborator_list_id"), table_name="collaborator")
    # ### end Alembic commands ###
