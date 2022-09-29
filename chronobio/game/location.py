from enum import IntEnum


class Location(IntEnum):
    FARM = 0
    FIELD1 = 1
    FIELD2 = 2
    FIELD3 = 3
    FIELD4 = 4
    FIELD5 = 5
    SOUP_FACTORY = 6


fields = (
    Location.FIELD1,
    Location.FIELD2,
    Location.FIELD3,
    Location.FIELD4,
    Location.FIELD5,
)
