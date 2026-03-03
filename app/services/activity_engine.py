class ActivityEngine:

    ACTIVITY_MATRIX = {
        "feed_pet": {"xp": 10, "health": 5, "happiness": 3, "energy": 5},
        "go_on_walk": {"xp": 20, "health": 10, "happiness": 10, "energy": -5},
        "bathe_pet": {"xp": 15, "health": 8, "happiness": 5, "energy": -2},
        "cuddle_time": {"xp": 10, "health": 0, "happiness": 12, "energy": -3},
        # "daily_prayer": {"xp": 50, "health": 3, "happines": 5, "energy":0},
        # "cuddle_time":  {"xp": 10, "health": 0, "happines": 12, "energy":-3},
    }

    def __init__(self, state):
        self.state = state

    def apply(self, activity_type: str):

        config = self.ACTIVITY_MATRIX.get(activity_type)
        if not config:
            raise ValueError("Invalid activity")

        self.state.xp += config["xp"]
        self.state.health = min(100, self.state.health + config["health"])
        self.state.happiness = min(100, self.state.happiness + config["happiness"])
        self.state.energy = max(0, self.state.energy + config["energy"])

        self._handle_growth()

        return {
            "xp_gained": config["xp"],
            "new_growth_level": self.state.growth_level,
            "new_health": self.state.health,
            "mood": self.state.mood,
        }

    def _handle_growth(self):
        if self.state.xp > self.state.growth_level * 200:
            self.state.growth_level += 1