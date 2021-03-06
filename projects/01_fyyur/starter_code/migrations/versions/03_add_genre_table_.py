"""empty message

Revision ID: 03_add_genre_table
Revises: 02_add_venue_fields_exc_genres
Create Date: 2020-12-24 12:37:52.424887

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = '03_add_genre_table'
down_revision = '02_add_venue_fields_exc_genres'
branch_labels = None
depends_on = None

conn = op.get_bind()
inspector = Inspector.from_engine(conn)
tables = inspector.get_table_names()


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    if 'genres' not in tables:
        genre = op.create_table('genres',
                                sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                                sa.Column('name', sa.String, nullable=False),
                                sa.PrimaryKeyConstraint('id'),
                                sa.UniqueConstraint('name')
                                )

    res = conn.execute("select * from genres")
    results = res.fetchall()

    if len(results) == 0:
        conn.execute("INSERT INTO genres(name) "
                     "VALUES('Alternative'), ('Blues'), ('Classical'), ('Country'), ('Electronic'),"
                     "('Folk'), ('Funk'), ('Hip-Hop'), ('Heavy Metal'), ('Instrumental'), ('Jazz'),"
                     "('Musical Theatre'), ('Pop'), ('Punk'), ('R&B'),"
                     "('Reggae'), ('Rock n Roll'), ('Soul'), ('Swing'), ('Other')")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    if 'venue_genres' in tables:
        op.drop_table('venue_genres')

    if 'artist_genres' in tables:
        op.drop_table('artist_genres')
    op.drop_table('genres')
    # ### end Alembic commands ###
