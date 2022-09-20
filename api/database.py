# """Code for database access (also creates some dummy data)."""
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from py_bank.service_layer import start_mappers, metadata


# engine = create_engine("sqlite:///jose_test.db", convert_unicode=True)
# metadata.create_all(engine)
# start_mappers()

# db_session = scoped_session(sessionmaker(bind=engine))

# Adding data
# db_session.execute("INSERT INTO Accounts (account_id, balance)" " VALUES (1, 1230.30)")
# db_session.execute("INSERT INTO Accounts (account_id, balance)" " VALUES (2, 40102.28)")

# db_session.execute(
#     "INSERT INTO Transfers (transfer_id, amount, transfer_type, src_account_id, dest_account_id)"
#     ' VALUES (1, 1203.23, "IntraBank", 2, 1)'
# )
# db_session.execute(
#     "INSERT INTO transfers (transfer_id, amount, transfer_type, src_account_id, dest_account_id)"
#     ' VALUES (2, 320.13, "IntraBank", 10, 1)'
# )
# db_session.commit()
