from sqlalchemy import UUID, DateTime, ForeignKey, String, Integer, Index, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

import uuid

class PetActivityLog(Base):
    __tablename__ = "pet_activity_log"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    pet_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pet.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    activity_type: Mapped[str] = mapped_column(String(30), nullable=False)
    activity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    partner_a_completed_at: Mapped[DateTime]
    partner_b_completed_at: Mapped[DateTime]

    xp_awarded: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        Index("ix_pet_activity_pet_activity", "pet_id", "activity_id"),
    )