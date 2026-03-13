from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, String, DateTime, Enum, func, Index, ForeignKey

from app.db.session import Base
from app.models.pet_state import PetStageEnum

import enum
import uuid

class CosmeticTypeEnum(str, enum.Enum):
    SKIN = "skin"
    ACCESSORY = "accessory"
    HAT = "hat"
    BACKGROUND = "background"


class PetCosmetic(Base):
    __tablename__ = "pet_cosmetic"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    type: Mapped[CosmeticTypeEnum] = mapped_column(
        Enum(CosmeticTypeEnum, name="cosmetic_type_enum")
    )

    required_stage: Mapped[PetStageEnum] = mapped_column(
        Enum(PetStageEnum, name="pet_stage_enum")
    )

    asset_key: Mapped[str] = mapped_column(String(100))  # sprite reference

    rarity: Mapped[str] = mapped_column(String(20), default="common")
    
    unlocks: Mapped[list["PetCosmeticUnlock"]] = relationship(
        "PetCosmeticUnlock",
        back_populates="cosmetic"
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
class PetCosmeticUnlock(Base):
    __tablename__ = "pet_cosmetic_unlock"

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

    cosmetic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pet_cosmetic.id", ondelete="CASCADE")
    )

    equipped: Mapped[bool] = mapped_column(default=False)

    unlock_source: Mapped[str] = mapped_column(
        String(30)
    )
    # examples:
    # "growth"
    # "streak"
    # "event"
    # "shop"
    # growth_level_5
    # weekly_event
    # streak_7
    # achievement

    unlocked_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    
    cosmetic: Mapped["PetCosmetic"] = relationship(
        "PetCosmetic",
        back_populates="unlocks"
    )

    __table_args__ = (
        Index("ix_pet_cosmetic_unique", "pet_id", "cosmetic_id", unique=True),
    )