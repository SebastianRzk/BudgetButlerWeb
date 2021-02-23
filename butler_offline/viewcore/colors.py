class GenericDesignColorChooser:
    def __init__(self, values, colors):
        self.values = sorted(values)
        self.colors = colors

    def get_for_value(self, value):
        index = self.values.index(value)
        color_index = index % len(self.colors)
        return '#' + self.colors[color_index]
