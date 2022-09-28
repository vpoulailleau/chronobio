from chronobio.game.constants import DAYS_OFF_PER_FIRE, DAYS_OFF_PER_FLOOD


class SoupFactory:
    def __init__(self):
        self.days_off = 0

    def flood(self):
        self.days_off += DAYS_OFF_PER_FLOOD

    def fire(self):
        self.days_off += DAYS_OFF_PER_FIRE
