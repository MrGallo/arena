class Stats:
    class Type:
        STR = "strength"
        AGI = "agility"
        INT = "intelligence"

    def __init__(self, str=10, agi=10, int=10):
        self.STR = str
        self.AGI = agi
        self.INT = int
    
    def __str__(self):
        return f"Stats(str={self.STR}, agi={self.AGI}, int={self.INT})"


class StatModifier:
    def __init__(self, affected_stat: Stats.Type, flat=0, percent=0.0, duration=0.0):
        """duration is in seconds.
        percent is 0.0 to 1.0
        one of flat and percent should be 0.
        """
        self.affected_stat = affected_stat
        self.flat = flat
        self.percent = percent
        self.remaining_frames = duration * 30  # game is in 30 frames per second


class ActiveModifiers:
    def __init__(self):
        self.modifier_list_map = {
            Stats.Type.STR: [],
            Stats.Type.AGI: [],
            Stats.Type.INT: [],
        }
    
    def add_stat_modifier(self, stat_modifier: StatModifier) -> None:
        self.modifier_list_map[stat_modifier.affected_stat].append(stat_modifier)
    
    def update(self):
        for lst in self.modifier_list_map.values():
            for modifier in lst:
                modifier.remaining_frames -= 1

            lst[:] = [m for m in lst if m.remaining_frames > 1]


class CalculatedStats(Stats):
    def __init__(self, base_stats, active_modifiers: ActiveModifiers):
        str_flat = sum(mod.flat for mod in active_modifiers.modifier_list_map[Stats.Type.STR])
        str_percent = sum(mod.percent for mod in active_modifiers.modifier_list_map[Stats.Type.STR])
        STR = (base_stats.STR + str_flat) * (1 + str_percent)
        
        agi_flat = sum(mod.flat for mod in active_modifiers.modifier_list_map[Stats.Type.AGI])
        agi_percent = sum(mod.percent for mod in active_modifiers.modifier_list_map[Stats.Type.AGI])
        AGI = (base_stats.AGI + agi_flat) * (1 + agi_percent)
        
        int_flat = sum(mod.flat for mod in active_modifiers.modifier_list_map[Stats.Type.INT])
        int_percent = sum(mod.percent for mod in active_modifiers.modifier_list_map[Stats.Type.INT])
        INT = (base_stats.INT + int_flat) * (1 + int_percent)

        super().__init__(STR, AGI, INT)

        # durability
        self.max_health = 100 + self.STR * 12
        self.health_regen = self.STR * 0.04

        # movement
        self.max_speed = 4.0 + self.AGI * 0.07
        self.accel_multiplier = 1.0 + self.AGI * 0.02

        # energy/stamina
        self.max_energy = 50 + self.STR * 4 + self.AGI * 2
        self.energy_regen = self.STR * 0.04 + self.AGI * 0.02
        self.energy_drain_mult = max(0.7, 1.0 - self.AGI * 0.01)

        # abilities
        self.ability_power = 1.0 + self.INT * 0.03
        self.cooldown_reduction = min(0.25, self.INT * 0.005)
    
