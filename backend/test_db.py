from sqlalchemy import create_engine
engine = create_engine('mysql://root:yixuanw99@127.0.0.1:3306/lucy_epigenetic')
connection = engine.connect()
print(connection)