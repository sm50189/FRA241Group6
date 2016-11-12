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

class Proposal(Base):

    __tablename__ = "Proposal"
    id = Column(Integer,primary_key= True)
    year = Column(Text)#ปีการศึกษา
    location = Column(Text)#สถานที่
    activity_location = Column(Text)#สถานที่จัดกิจกรรม/สถานที่ดำเนินงาน/สถานที่ปฏิบัติงาน
    Reason = Column(Text)#หลักการ และเหตุผล

    objective = relationship("Objective", back_populates = "parent_proposal")#วัตถุประสงค์

    activity_comparition = Column(Text)#การเทียบค่ากิจกรรม
    duration = Column(Text)#ระยะเวลาดำเนินงาน

    owner_for_proposal = relationship("Owner_for_proposal",back_populates = "parent_proposal")#ผู้รับผิดชอบ
    member_for_proposal = relationship("Member_for_proposal",back_populates = "parent_proposal")#ผู้เข้าร่วม

    number_of_member = Column(Integer)
    evaluation_index = Column(Text)#รูปแบบการประเมินผล
    profit = Column(Text)#ประโบชน์ที่คาดว่าจะได้รับ/ผลที่คาดว่าจะได้รับ
    type_of_activity = Column(Text)#ลักษณะกิจกรรม/ลักษณะการปฏิบัติงาน

    cost = relationship("Cost",back_populates="parent_proposal")#ค่าใช้จ่ายในการจัดกิจกรรม
    delicate_budget = relationship("Delicate_budget",back_populates = "parent_proposal")#งบประมาณโดยละเอียด

    success_criteria = Column(Text)#ตัวชี้วัดความสำเร็จของโครงการ

    schedule = relationship("Schedule",back_populates = "parent_proposal")#ตารางการดำเนินกิจกกรม
    previouse_result = relationship("Previouse_result",back_populates = "parent_proposal")#ผลการจัดที่ผ่านมา

    parent_id = Column(Integer, ForeignKey("Project.id"))
    parent_project = relationship("Project", back_populates = "proposal", uselist = False)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass



class Objective(Base):
    __tablename__ = "Objective"
    id = Column(Integer , primary_key=True)
    text = Column(Text)

    proposal_id = Column(Integer,ForeignKey("Proposal.id"))
    parent_proposal = relationship("Proposal", back_populates="objective")

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class Cost(Base):
    __tablename__ = "Cost"
    id = Column(Integer,primary_key=True)
    text  =Column(Text)

    proposal_id = Column(Integer,ForeignKey("Proposal.id"))
    parent_proposal = relationship("Proposal",back_populates="cost")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class Previouse_result(Base):
    __tablename__ = "Previouse_result"
    id = Column(Integer,primary_key=True)
    text = Column(Text)

    proposal_id = Column(Integer,ForeignKey("Proposal.id"))
    parent_proposal = relationship("Proposal",back_populates = "previouse_result")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class Owner_for_proposal(Base):
    __tablename__ = "Owner_for_proposal"
    id = Column(Integer,primary_key=True)
    text = Column(Text)

    proposal_id = Column(Integer, ForeignKey("Proposal.id"))
    parent_proposal = relationship("Proposal",back_populates="owner_for_proposal")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class Member_for_proposal(Base):
    __tablename__ = "Member_for_proposal"
    id = Column(Integer,primary_key=True)
    text = Column(Text)

    proposal_id = Column(Integer, ForeignKey("Proposal.id"))
    parent_proposal = relationship("Proposal",back_populates = "member_for_proposal")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class Delicate_budget(Base):
    __tablename__ = "Delicate_budget"
    id = Column(Integer,primary_key=True)
    order = Column(Text)#ลำดับ
    descrip = Column(Text)#รายละเอียด
    value = Column(Text)#จำนวนเงิน

    proposal_id = Column(Integer, ForeignKey("Proposal.id"))
    parent_proposal = relationship("Proposal",back_populates = "delicate_budget")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class Schedule(Base):
    __tablename__ = "Schedule"
    id = Column(Integer,primary_key=True)
    time = Column(Text)
    descrip = Column(Text)

    proposal_id = Column(Integer, ForeignKey("Proposal.id"))
    parent_proposal = relationship("Proposal",back_populates = "schedule")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass