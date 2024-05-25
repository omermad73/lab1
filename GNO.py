class GNO: #Generic Networking Object
    Count_Objects = 0

    def __init__(self, type):
        self.id = GNO.Count_Objects
        self.type = type
        GNO.Count_Objects += 1
