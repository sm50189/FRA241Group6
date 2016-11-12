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

class Obligation(Base):

    __tablename__ = "Obligation"
    id = Column(Integer, primary_key=True)
    type = Column(VARCHAR(20))
    description = Column(Text)
    duty = Column(Text)
    status = Column(VARCHAR(20))

    project_id = Column(Integer, ForeignKey("Project.id"))
    asso_to = relationship('Project', back_populates = "project_obligation")

    equipment_id = Column(Integer,ForeignKey("Equipment.id"))
    equipment = relationship("Equipment", back_populates = "as_obligation")
