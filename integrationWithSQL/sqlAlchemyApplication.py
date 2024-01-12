from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import inspect

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    # attribute
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    
    
    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )
    
class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")
    
    def __repr__(self):
        return f"Address (id={self.id}, email={self.email_address})"
    
    
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

# Creating a session to persist data in SQLite
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