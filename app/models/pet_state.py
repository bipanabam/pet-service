
# # {
# #   "pet_id": "uuid",
# #   "name": "Lumi",
# #   "stage": "teen",
# #   "xp": 1240,
# #   "growth_level": 5,
# #   "health": 82,
# #   "happiness": 74,
# #   "energy": 61,
# #   "mood": "happy",
# #   "version": 12,
# #   "last_interaction_at": "timestamp",
# #   "cosmetics": {
# #     "skin": "default",
# #     "accessory": "crown"
# #   },
# #   "active_boosts": [
# #     {
# #       "type": "weekly_challenge",
# #       "multiplier": 1.5,
# #       "expires_at": "timestamp"
# #     }
# #   ]
# # }

from sqlalchemy import Integer, String, DateTime, ForeignKey, Index, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.session import Base
import uuid
import enum

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.pet import Pet

class PetStageEnum(str, enum.Enum):
    EGG = "egg"
    BABY = "baby"
    TEEN = "teen"
    ADULT = "adult"

class PetState(Base):
    __tablename__ = "pet_state"

    pet_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pet.id", ondelete="CASCADE"),
        primary_key=True
    )

    stage: Mapped[PetStageEnum] = mapped_column(
        Enum(
            PetStageEnum,
            name="pet_stage_enum",
            create_constraint=True
        ),
        nullable=False
    )
    xp: Mapped[int] = mapped_column(Integer, default=0)
    growth_level: Mapped[int] = mapped_column(Integer, default=1)

    health: Mapped[int] = mapped_column(Integer, default=100)
    happiness: Mapped[int] = mapped_column(Integer, default=100)
    energy: Mapped[int] = mapped_column(Integer, default=100)

    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    last_interaction_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    pet: Mapped["Pet"] = relationship("Pet", back_populates="state")

    __table_args__ = (
        Index("ix_pet_state_health", "health"),
    )
    
    @property
    def mood(self) -> str:
        if self.health < 30:
            return "sick"
        elif self.happiness > 80 and self.energy > 80:
            return "happy"
        elif self.happiness < 40:
            return "sad"
        elif self.energy < 40:
            return "tired"
        else:
            return "neutral"