from sqlalchemy import Column, String
from app.db.base_class import Base
class DiagnoseCodeTable(Base):

    __tablename__ = 'diagnose_code_table'
    code_id = Column(String, primary_key=True)
    diagnosis = Column(String)
