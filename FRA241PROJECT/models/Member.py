from sqlalchemy import (
    Table,
    Column,
    Index,
    Integer,
    Text,
    VARCHAR,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from .meta import Base

Member_table = Table('Member_table', Base.metadata,
    Column('Project_id', Integer, ForeignKey('Project.id')),
    Column('User_id', Integer, ForeignKey('User.id'))
)

Advisor_table  = Table('Advisor_table', Base.metadata,
    Column('Project_id', Integer, ForeignKey('Project.id')),
    Column('User_id', Integer, ForeignKey('User.id'))
)