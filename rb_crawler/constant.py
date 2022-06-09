import enum

BOOTSTRAP_SERVER: str = "localhost:29092"
SCHEMA_REGISTRY_URL: str = "http://localhost:8081"
RB_ANNOUNCEMENTS: str = "rb-announcements"
RB_CORPORATES: str = "rb-corporates"
RB_PERSONS: str = "rb-persons"


class State(str, enum.Enum):
    BADEN_WUETTEMBERG = "bw"
    BAYERN = "by"
    BERLIN = "be"
    BRANDENBURG = "br"
    BREMEN = "hb"
    HAMBURG = "hh"
    HESSEN = "he"
    MECKLENBURG_VORPOMMERN = "mv"
    NIEDERSACHSEN = "ni"
    NORDRHEIN_WESTFALEN = "nw"
    RHEILAND_PFALZ = "rp"
    SAARLAND = "sl"
    SACHSEN = "sn"
    SACHSEN_ANHALT = "st"
    SCHLESWIG_HOLSTEIN = "sh"
    THUERINGEN = "th"
