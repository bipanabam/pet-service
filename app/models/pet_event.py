from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, Index, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base

class PetEvent(Base):
    __tablename__="pet_event"
       
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    ) # Idempotency-Key
    
    pet_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pet.id", ondelete="CASCADE"),
        nullable=False,
        index=True  
    )
    
    activity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )
    
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    