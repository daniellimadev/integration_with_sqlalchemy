import sqlalchemy as sqlA
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column, create_engine, inspect, select, func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey


Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"
    # attribute
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship("Address", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")
    
    def __repr__(self):
        return f"Address(id={self.id}, email={self.email_address})"
    
print(User.__tablename__)
print(Address.__tablename__)

# connection to the database
engine = create_engine("sqlite://")

# Creating classes as tables in the database
Base.metadata.create_all(engine)

# Investigate the database schema
inspect_engine = inspect(engine)
print(inspect_engine.has_table("user_account"))

print(inspect_engine.get_table_names())
print(inspect_engine.default_schema_name)

with Session(engine) as session:
    daniel = User(
        name='daniel',
        fullname='Daniel Pereira',
        address=[Address(email_address='daniel@gmail.com')]
    )
    
    aline = User(
        name='aline',
        fullname='Aline Barbosa',
        address=[Address(email_address='aline1@gmail.com'),
                 Address(email_address='aline2@email.org')]
    )
    
    debora = User(name='debora', fullname='Debora Barbosa')
    
    # sending to the database (data persistence)
    session.add_all([daniel, aline, debora])
    session.commit()

stmt = select(User).where(User.name.in_(['ariel', 'mirella']))
print('Recovering users from a filtered condition')
for user in session.scalars(stmt):
    print(user)

stm_address = select(Address).where(Address.user_id.in_([2]))
print("Recovering Mirella's email addresses")
for address in session.scalars(stm_address):
    print(address)

stmt_order = select(User).order_by(User.fullname.desc())
print('\nRetrieving information in an orderly manner')
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
for result in session.scalars(stmt_join):
    print(result)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print('\nExecuting statement from connection')
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(User)
print('\nTotal instances in User')
for result in session.scalars(stmt_count):
    print(result)
