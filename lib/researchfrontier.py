class ResearchFrontier:
    def __init__(self, name, size, classification):
        self.name = name
        self.size = size
        self.classification = classification
        self.growth = 0
        self.impact = 0
        self.sci = 0
        

    def description(self):
        return """ Name: {self.name} \n
                 Number of Publications: {self.name} \n
                 Classification: {self.classification} \n
                 Growth Index: {self.growth} \n
                 Impact Index: {self.impact} \n
                 Sci-based Index: {self.sci} \n
                 """