from sqlalchemy import UUID, Enum, DateTime, ForeignKey, String, Integer, Index, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

import uuid
import enum

class ActivityTypeEnum(str, enum.Enum):
    FEED_PET = "feed_pet"
    WALK_PET = "walk_pet"
    BATHE_PET = "bathe_pet"
    CUDDLE_PET = "cuddle_pet"
    PLAY_WITH_PET = "play_with_pet"
    TRAIN_PET = "train_pet"
    
class PetActivity(Base):
    __tablename__ = "pet_activity"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    pet_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pet.id", ondelete="CASCADE"),
        index=True
    )

    activity_type: Mapped[ActivityTypeEnum] = mapped_column(
        Enum(
        ActivityTypeEnum,
        name="activity_type_enum",
        create_constraint=True
        ),
        nullable=False
    )
    activity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    xp_awarded: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        Index("ix_unique_pet_activity", "pet_id", "activity_id", unique=True),
    )
    
class PetActivityParticipant(Base):
    __tablename__ = "pet_activity_participant"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    activity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pet_activity.id", ondelete="CASCADE"),
        index=True
    )

    partner_id: Mapped[str] = mapped_column(String, index=True)

    completed_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        Index(
            "ix_unique_activity_partner",
            "activity_id",
            "partner_id",
            unique=True
        ),
    )