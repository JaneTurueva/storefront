from sqlalchemy import create_engine


# def test_db_query(temp_migrated_db: str):
#     engine = create_engine(temp_migrated_db)
#     with engine.connect() as conn:
#         value = conn.execute('SELECT 1').scalar()
#         assert value is 1