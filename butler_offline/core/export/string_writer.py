class StringWriter:

    def __init__(self):
        self.value = ""

    def write(self, new_line):
        self.value = self.value + new_line

    def write_line(self, new_line):
        self.write(str(new_line) + '\n')

    def write_empty_line(self, count=1):
        self.write('\n' * count)

    def to_string(self):
        return self.value
