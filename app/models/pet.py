
# # {
# #   "pet_id": "uuid",
# #   "name": "Lumi",
# #   "pet_type": "spirit",
# #   "initial_stage": "egg",
# #   "health": 100,
# #   "xp": 0
# # }
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Index, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.session import Base
from typing import TYPE_CHECKING

import uuid

if TYPE_CHECKING:
    from app.models.pet_state import PetState
    from app.models.couple import Couple

class Pet(Base):
    __tablename__="pet"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    couple_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("couple.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    pet_type: Mapped[str] = mapped_column(String(30), nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    # relationships
    couple: Mapped["Couple"] = relationship("Couple", back_populates="pets")
    state: Mapped["PetState"] = relationship(
        "PetState",
        back_populates="pet",
        uselist=False,
        cascade="all, delete-orphan"
    )