from chronobio.game.field import Field


class Farm:
    def __init__(self: "Farm") -> None:
        self.blocked = True
        self.name = "En construction"
        self.money = 100_000
        self.fields = [Field() for _ in range(5)]
