

class Token:
    END = 0
    ID = 1
    def __init__(self, id, value=None):
        self.id = id
        self.value = value

    def __repr__(self):
        if self.value != None:
            print("{}({})".format(self.id, self.value))
        else:
            print(self.id)
