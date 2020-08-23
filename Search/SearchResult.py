from datetime import datetime

class SearchResult:
    search: str
    timestamp: int
    date: datetime

    def __init__(self, se: str, da):
        self.search = str(se).lower()
        self.timestamp = da
        self.date = datetime.fromtimestamp(da)

    def toString(self) -> str:
        return str(self.date) + '\t\t' + self.search

