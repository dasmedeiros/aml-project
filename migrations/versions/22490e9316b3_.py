"""empty message

Revision ID: 22490e9316b3
Revises: 78f215e25e91
Create Date: 2023-08-31 15:11:18.703956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22490e9316b3'
down_revision = '78f215e25e91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('accounts', schema=None) as batch_op:
        batch_op.alter_column('balance',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    with op.batch_alter_table('merchants', schema=None) as batch_op:
        batch_op.alter_column('long',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)
        batch_op.alter_column('lat',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.alter_column('long',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)
        batch_op.alter_column('lat',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)
        batch_op.alter_column('amount',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)
        batch_op.alter_column('movement',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=1),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.alter_column('movement',
               existing_type=sa.String(length=1),
               type_=sa.VARCHAR(length=10),
               existing_nullable=False)
        batch_op.alter_column('amount',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)
        batch_op.alter_column('lat',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)
        batch_op.alter_column('long',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    with op.batch_alter_table('merchants', schema=None) as batch_op:
        batch_op.alter_column('lat',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)
        batch_op.alter_column('long',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    with op.batch_alter_table('accounts', schema=None) as batch_op:
        batch_op.alter_column('balance',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    # ### end Alembic commands ###
