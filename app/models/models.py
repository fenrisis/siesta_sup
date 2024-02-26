from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./siesta_sup.db"
engine = create_async_engine(DATABASE_URL, echo=True)
metadata = MetaData()
Base = declarative_base(metadata=metadata)


roles_table = Table('roles', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String(50)),
                    Column('permissions', JSON))

users_table = Table('siesta_users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String(50)),
                    Column('phone', String(20)),
                    Column('telegram_id', Integer),
                    Column('telegram_name', String(50)),
                    Column('role_id', ForeignKey('roles.id')))

sups_table = Table('sups', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String(50)),
                   Column('picture', String),
                   Column('price', Integer),
                   Column('quantity', Integer))

rents_table = Table('rents', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('user_id', ForeignKey('siesta_users.id')),
                    Column('sup_id', ForeignKey('sups.id')),
                    Column('rent_start', String),
                    Column('rent_end', String))


class Role(Base):
    __table__ = roles_table
    users = relationship("User", back_populates="role")


class User(Base):
    __table__ = users_table
    role = relationship("Role", back_populates="users")
    rents = relationship("Rent", back_populates="user")

class Sup(Base):
    __table__ = sups_table
    rents = relationship("Rent", back_populates="sup")

class Rent(Base):
    __table__ = rents_table
    user = relationship("User", back_populates="rents")
    sup = relationship("Sup", back_populates="rents")


