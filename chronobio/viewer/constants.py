import arcade


class Constants:
    SCREEN_WIDTH = 1777
    SCREEN_HEIGHT = 1000
    SCREEN_TITLE = "Chronobio"

    EVENT_VISIBILITY_NB_DAYS = 40

    COLORS = [
        (0xB5, 0x89, 0x00),
        (0x6C, 0x71, 0xC4),
        (0xCB, 0x4B, 0x16),
        (0x26, 0x8B, 0xD2),
        (0xDC, 0x32, 0x2F),
        (0x2A, 0xA1, 0x98),
        (0xD3, 0x36, 0x82),
        (0x85, 0x99, 0x00),
        arcade.color.BROWN_NOSE,
    ]

    def __init__(self):
        self.resize(width=1777, height=1000)

    def resize(self, width: int, height: int) -> None:
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height

        self.FARM_LENGTH = self.SCREEN_WIDTH * 0.3

        self.SOUP_FACTORY_DISTANCE_FROM_CENTER = self.FARM_LENGTH
        self.SOUP_FACTORY_WIDTH = self.FARM_LENGTH / 6

        self.FIELD_OFFSET = self.FARM_LENGTH / 7 * 2
        self.FIELD_WIDTH = self.FARM_LENGTH / 8
        self.FIELD_DISTANCE = self.FARM_LENGTH / 7

        self.FARM_BUILDING_DISTANCE_FROM_CENTER = self.FARM_LENGTH / 7
        self.FARM_BUILDING_WIDTH = self.FARM_LENGTH / 7


constants: Constants = Constants()
