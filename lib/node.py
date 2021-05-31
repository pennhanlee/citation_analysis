class Node:
    def __init__(self, title, abstract, keywords, year, journal, timesCited, timesCiting):
        self.title = title
        self.abstract = abstract
        self.keywords = keywords
        self.year = year
        self.journal = journal
        self.timesCited = timesCited
        self.timesCiting = timesCiting

    def description(self):
        return """Title: {self.title} \n
                  Year: {self.year} \n
                  Abstract: {self.abstract} \n
                  Journal: {self.journal} \n
                  Times Cited: {self.timesCited} \n
                  Times Citing: {self.timesCiting} \n
                """