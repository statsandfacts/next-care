from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship


class UserRole(Base):
    __tablename__ = "user_roles"
    user_id = Column(
        CHAR(36),
        ForeignKey("user.user_id"),
        primary_key=True,
        nullable=False,
    )
    role_id = Column(
        CHAR(36),
        ForeignKey("roles.role_id"),
        primary_key=True,
        nullable=False,
    )

    role = relationship("Role")
    user = relationship("User", back_populates="user_role", uselist=False)

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="unique_user_role"),
    )
