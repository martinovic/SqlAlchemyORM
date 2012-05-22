from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.sql import select

def createDatabase():
    """
    Creates a simple user database and returns
    the engine, metadata and users_table
    """
    engine = create_engine('sqlite:///tutorial.db',
                           echo=True)

    metadata = MetaData(bind=engine)

    users_table = Table('users', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('name', String(40)),
                        Column('age', Integer),
                        Column('password', String),
                        )
    
    addresses_table = Table('addresses', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('user_id', None, ForeignKey('users.id')),
                            Column('email_address', String, nullable=False)                            
                            )

    
    # create tables in database
    metadata.create_all()
    
    return engine, metadata, users_table

def insertExample(engine, users_table):
    # create an Insert object
    ins = users_table.insert()
    # add values to the Insert object
    new_user = ins.values(name="Joe", age=20, password="pass")
    
    # create a database connection
    conn = engine.connect()
    # add user to database by executing SQL
    conn.execute(new_user)
    
    # add multiple users at once
    conn.execute(users_table.insert(), [
        {"name": "Ted", "age":10, "password":"dink"},
        {"name": "Asahina", "age":25, "password":"nippon"},
        {"name": "Evan", "age":40, "password":"macaca"}
    ])
    
    
    # a connectionless way to Insert a user
    ins = users_table.insert()
    result = engine.execute(ins, name="Shinji", age=15, password="nihongo")
    
    # another connectionless Insert
    result = users_table.insert().execute(name="Martha", age=45, password="dingbat")


def selectExample(engine, users_table):
    """
    Shows various select examples
    """
    # Do a Select all (SELECT * FROM users)
    s = select([users_table])
    result = s.execute()
    
    for row in result:
        print row
    
    # just get the first result
    conn = engine.connect()
    res = conn.execute(s)
    row = res.fetchone()
    print row
    
    # get all the results in a list of tuples
    res = conn.execute(s)
    rows = res.fetchall()
    
    # limit the number of columns returned
    s = select([users_table.c.name, users_table.c.age])
    result = conn.execute(s)
    for row in result:
        print row
        
    # The following is the equivalent to 
    # SELECT * FROM users WHERE name=="Martha"
    s = select([users_table], users_table.c.name == "Martha")
    
    # The following is the equivalent to 
    # SELECT * FROM users WHERE id > 3
    s = select([users_table], users_table.c.id > 3)
    
    # You can use the "and_" module to AND multiple fields together
    # and SqlAlchemy supports the "like" paradigm too!
    # Note that this particular query doesn't return anything
    s = s.select(and_(users_table.c.name.like('T%'), users_table.c.age < 25))

if __name__ == "__main__":
    engine, metadata, users_table = createDatabase()
    