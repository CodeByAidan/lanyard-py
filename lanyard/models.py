from typing import Optional, TypedDict


class PartialUser(TypedDict):
    username: str
    public_flags: int
    id: str
    discriminator: str
    bot: bool
    avatar: str


class PartialPresence(TypedDict):
    spotify: str
    discord_user: PartialUser
    kv: dict
    listening_to_spotify: bool
    activities: list
    discord_status: str


class Presence:
    def __init__(self, data: PartialPresence):
        self._update(data)

    def _update(self, data: PartialPresence):
        self.username = data["discord_user"]["username"]
        self.public_flags = data["discord_user"]["public_flags"]
        self.id = data["discord_user"]["id"]
        self.discriminator = data["discord_user"]["discriminator"]
        self.bot = data["discord_user"]["bot"]
        self.avatar = data["discord_user"]["avatar"]
        self.activites = data["activities"]
        self.spotify = data["spotify"]
        self.currently_listening = data["listening_to_spotify"]
        self.kv = data["kv"]
        self.status = data["discord_status"]

    def __repr__(self):
        return f"<{self.__class__.__name__}: username: {self.username!r} id: {self.id} status: {self.status!r}>"