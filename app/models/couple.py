# Sync pair table created in Appwrite
from dataclasses import Field
import uuid

from sqlalchemy import DateTime, String, UUID, func
from sqlalchemy.orm import relationship,Mapped, mapped_column
from app.db.session import Base

from app.models.pet import Pet

class Couple(Base):
    __tablename__ = "couple"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )

    pair_id: Mapped[str] = mapped_column(String, index=True, unique=True) # This is the ID from Appwrite, used for syncing and reference
    
    partnerOne_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    partnerTwo_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    #relationships
    pets: Mapped[list[Pet]] = relationship(
        back_populates="couple", 
        cascade="all, delete-orphan"
    )
    
    
