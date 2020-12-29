import numbers

class Radical(numbers.Real):

    __slots__ = ("radicand", "degree")

    def __init__(self, radicand, degree):  # radicand ** (1/degree)
        self.radicand = radicand
        self.degree = degree

    def __float__(self):
        return pow(self.radicand, 1 / self.degree)

    def __eq__(self, other):
