from enum import Enum


class Role(Enum):
    ADMINS = "Admins"
    APPRAISER = "Appraiser"
    BOT_DEV = "Bot Dev"


class Channel(Enum):
    LOBBY = "lobby"
