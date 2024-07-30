from dataclasses import dataclass
@dataclass
class dbc:
    database: str
    dbhost: str
    dbport: int
    dbuser: str
    dbpassword: str


@dataclass
class webdb:
    webhost: str
    webport: int
    webuser: str
    webpassword: str
    database: str

@dataclass
class entity:
    identity: str
    platform: list
    reputation: float

@dataclass
class route:
    community: str
    platform: str
    interface: str
    subInterface: str
