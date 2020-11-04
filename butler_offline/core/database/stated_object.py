
class StatedObject:

    def __init__(self):
        self.tainted = 0

    def taint(self):
        self.tainted = self.tainted + 1

    def taint_number(self):
        return self.tainted
