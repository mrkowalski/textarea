import re
from enum import Enum

class Command(Enum):
    TRANSLATE = 1
    BOOKMARK = 2

class Parser:

    rx_prefix = re.compile("^https?://.*", re.I)

    def __init__(self):
        self.tld = []
        with open("app/tld.txt") as f:
            for line in f:
                if not line.startswith("#"):
                    self.tld.append(line.strip().lower())
        self.rx_tld = re.compile("(" + "|".join([f"(\\.{s})" for s in self.tld]) + ")(?![a-z0-9.])")

    def has_url_prefix(self, s: str):
        return self.rx_prefix.match(s.strip().lower()) is not None

    def is_url(self, s: str):
        s = s.strip().lower()
        if self.rx_prefix.match(s) is not None:
            return True
        elif self.rx_tld.search(s) is not None:
            return True
        else:
            return False

    def get_command(self, s: str):
        bits = s.split(" ")
        if len(bits) > 1:
            if (bits[0] == "t"):
                return (Command.TRANSLATE, " ".join(bits[1:]))
        elif len(bits) == 1:
            if  len(bits[0]) == 2:
                if bits[0] == "fb":
                    return (Command.BOOKMARK, "https://facebook.com")
                elif bits[0] == "rp":
                    return (Command.BOOKMARK, "https://rp.pl")
        return None


# https://data.iana.org/TLD/tlds-alpha-by-domain.txt
