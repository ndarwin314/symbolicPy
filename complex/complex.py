# TODO make binary operations for stuff like reals

from abstract.complex.quaternion import Quaternion

class Complex(Quaternion):

    def __init__(self, components):
        super().__init__([components[0], components[1], 0, 0])

    def __repr__(self):
        return str(self.real) + " + " + str(self.imag) + "i"

    def __mul__(self, other):
        if isinstance(other, Complex):
            return Complex([self.real * other.real - self.imag * other.imag,
                            self.real * other.imag + self.imag * other.real])

    def __add__(self, other):
        if isinstance(other, Complex):
            return Complex([self.real + other.real, self.imag + other.imag])

    def __len__(self):
        return self