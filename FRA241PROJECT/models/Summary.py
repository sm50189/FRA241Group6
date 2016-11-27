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

class Summary(Base):

    __tablename__ = "Summary"
    id = Column(Integer,primary_key=True)
    owner_for_proposal = Column(Text)  # ผู้รับผิดชอบ
    member_for_proposal = Column(Text)  # ผู้เข้าร่วม
    Reason = Column(Text)  # หลักการ และเหตุผล
    objective = Column(Text)  # วัตถุประสงค์
    target_group = Column(Text) #กลุ่มเป้าหมาย
    profit = Column(Text) ##ผลที่คาดว่าจะได้รับ,ประโบชน์ที่คาดว่าจะได้รับ
    delicate_budget = Column(Text) #งบประมาณโดยละเอียด/งบประมาณที่ใช้
    location = Column(Text) #สถานที่ปฏิบัติงานและระยะเวลาในการดำเนินกิจกรรม
    problem = Column(Text) #ปัญหาและอุปสรรคในการดำเนินกิจกรรม
    suggest = Column(Text) #ข้อเสนอแนะในการดำเนินโครงการครั้งต่อไป
    criteria = Column(Text) #การประเมินโครงการ

    parent_id = Column(Integer, ForeignKey("Project.id"))
    parent_project = relationship("Project", back_populates="summary")