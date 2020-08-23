from DateTime import DateTime

class SearchResult:
    search: str
    date: DateTime

    def __init__(self, se: str, da):
        self.search = str(se).lower()
        self.date = DateTime(da)

    def toString(self) -> str:
        return str(self.date) + '\t\t' + self.search

