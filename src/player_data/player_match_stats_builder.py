class PlayerMatchStatsBuilder:

    def __init__(self):
        self.stat_profile = {}

    def add_match_stat(self, stat, value):
        self.stat_profile[stat], value


