from sqlalchemy import (
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

import datetime

class Equipment(Base):
    __tablename__ = "Equipment"
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50))
    cost = Column(Integer)
    buy_date = Column(Date)
    contract = Column(VARCHAR(50))
    status = Column(VARCHAR(20))

    from_project = Column(Integer, ForeignKey("Project.id"))
    asso_to =  relationship("Project", back_populates = "project_equipment")

    as_obligation = relationship("Obligation", back_populates="equipment")

    owner_id = Column(Integer , ForeignKey("User.id"))
    owner = relationship("User", back_populates = "own_euipment")