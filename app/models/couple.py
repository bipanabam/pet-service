# Sync pair table created in Appwrite
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import relationship,Mapped, mapped_column
from app.db.session import Base

from app.models.pet import Pet

class Couple(Base):
    __tablename__ = "couple"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True
    )# id from pair table in appwrite
    
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
    
    
