from app.models.pet_cosmetic import CosmeticTypeEnum
from app.models.pet_state import PetStageEnum
from app.models.pet_cosmetic import CosmeticRarityEnum


COSMETIC_CATALOG = [

    {
        "name": "default_skin",
        "type": CosmeticTypeEnum.SKIN,
        "required_stage": PetStageEnum.EGG,
        "asset_key": "skin_default",
        "rarity": CosmeticRarityEnum.COMMON,
    },

    {
        "name": "baby_scarf",
        "type": CosmeticTypeEnum.ACCESSORY,
        "required_stage": PetStageEnum.BABY,
        "asset_key": "accessory_baby_scarf",
        "rarity": CosmeticRarityEnum.COMMON,
    },
    
    {
        "name": "flower_crown",
        "type": CosmeticTypeEnum.HAT,
        "required_stage": PetStageEnum.BABY,
        "asset_key": "hat_flower_crown",
        "rarity": CosmeticRarityEnum.COMMON,
    },

    {
        "name": "golden_crown",
        "type": CosmeticTypeEnum.HAT,
        "required_stage": PetStageEnum.TEEN,
        "asset_key": "hat_golden_crown",
        "rarity": CosmeticRarityEnum.RARE,
    },
    
    {
        "name": "devil_horns",
        "type": CosmeticTypeEnum.ACCESSORY,
        "required_stage": PetStageEnum.TEEN,
        "asset_key": "accessory_devil_horns",
        "rarity": CosmeticRarityEnum.RARE,
    },
    
    {
        "name": "space_background",
        "type": CosmeticTypeEnum.BACKGROUND,
        "required_stage": PetStageEnum.TEEN,
        "asset_key": "background_space_background",
        "rarity": CosmeticRarityEnum.RARE,
    },

    {
        "name": "angel_wings",
        "type": CosmeticTypeEnum.ACCESSORY,
        "required_stage": PetStageEnum.ADULT,
        "asset_key": "accessory_angel_wings",
        "rarity": CosmeticRarityEnum.EPIC,
    },
]