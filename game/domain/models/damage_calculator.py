class DamageCalculator:
    @staticmethod
    def physical(attacker, defender, base_damage):
        atk = attacker.stats.atk
        defense = defender.stats.defense
        return base_damage * (3 * atk) / (2 * atk + defense)

    @staticmethod
    def magical(attacker, defender, base_damage):
        atk = attacker.stats.magic_atk
        defense = defender.stats.magic_resistance
        return base_damage * (3 * atk) / (2 * atk + defense)
    
