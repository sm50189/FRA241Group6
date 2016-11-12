# -- coding: utf-8 --
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
from .Member import Member_table,Advisor_table

class Project(Base):

    __tablename__ = "Project"
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    description = Column(Text)
    status = Column(VARCHAR(20))
    type = Column(VARCHAR(20))
    # activity_date = Column(Date)
    start_date = Column(Date)
    finish_date = Column(Date)

    owner_id = Column(Integer,ForeignKey('User.id'))
    leader = relationship("User", back_populates = "own_project")#ผู้รับผิดชอบ

    # Advisor_id = Column(Integer,ForeignKey('User.id'))
    advisor = relationship("User", secondary = Advisor_table,back_populates = "advisee_project")

    project_member = relationship("User", secondary = Member_table, back_populates = "enroll_project" )

    project_obligation = relationship("Obligation", back_populates = "asso_to")

    project_equipment = relationship("Equipment", back_populates = "asso_to")


    proposal = relationship("Proposal",back_populates = "parent_project")

    def change_status(self,status):
        self.status = status

    def change_description(self, description):
        self.description = description

    def enroll_member(self, member):
        self.project_member.append(member)

    def promote_leader(self, leader):
        self.leader = leader

    def finish_project(self):
        pass

    def is_finish(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

