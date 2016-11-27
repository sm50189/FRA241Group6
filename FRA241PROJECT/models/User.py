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

import bcrypt


class User(Base):
     __tablename__ = "User"
     id = Column(Integer, primary_key=True)
     First_name = Column(VARCHAR(30))
     Last_name = Column(VARCHAR(30))
     role = Column(VARCHAR(10))
     student_id = Column(Integer, nullable= True)
     password = Column(VARCHAR(20))
     Email = Column(VARCHAR(50))
     user_id = Column(VARCHAR(20))
     year = Column(Integer, nullable=True)

     own_project = relationship("Project", back_populates = "leader")

     advisee_project = relationship("Project", secondary = Advisor_table,back_populates = "advisor")

     enroll_project = relationship("Project", secondary=Member_table, back_populates = "project_member")

     own_euipment = relationship("Equipment", back_populates = "owner")

     own_comment = relationship("Comment",back_populates = "writer")

     def hash_password(self,password):
         password_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
         self.password = password_hash

     def check_password(self, password):

         if self.password is not None:
             expected_hash = self.password.encode('utf8')
             return bcrypt.checkpw(password.encode('utf8'),expected_hash)

         return False

     def change_password(self,password):
         self.hash_password(password)

     def __enter__(self):
        return self
     def __exit__(self, exc_type, exc_val, exc_tb):
         pass
