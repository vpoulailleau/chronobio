from chronobio.game.location import Location


class Employee:
    def __init__(self, id):
        self.id = id
        self.location = Location.FARM
        self.days_off = 0
        self.tractor = None

    def move(self, target: Location) -> None:
        distance = abs(target - self.location)
        sign = 1 if target > self.location else -1
        if not distance:
            return
        if self.tractor is None:
            self.days_off = distance - 1
            self.location += sign
        else:
            self.days_off = (distance - 1) // 3
            if distance > 3:
                self.location += sign * 3
            else:
                self.location = target
            self.tractor.location = self.location

        # clamp location to valid location
        if self.location < Location.FARM:
            self.location = Location.FARM
        if self.location > Location.SOUP_FACTORY:
            self.location = Location.SOUP_FACTORY
