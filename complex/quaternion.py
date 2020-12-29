import numpy as np
import numbers
import collections.abc
# TODO: add iterable to class

class Quaternion(numbers.Complex, collections.abc.Iterable):

    __slots__ = ("_real", "_imag", "j", "k",)

    def __init__(self, components):
        if len(components) != 4:
            raise IndexError("Must be length 4")
        # TODO check elements are numbers
        self._real = components[0]
        self._imag = components[1]
        self.j = components[2]
        self.k = components[3]
        self.vector = np.array((self.real, self.imag, self.j, self.k))
        self.imaginary = self.vector[1:]
        self._imagNorm = None
        self._norm = None

    def __iter__(self):
        return iter(self.vector)

    def __getitem__(self, item):
        return self.vector[item]

    @classmethod
    def from_complex(cls, number):
        if isinstance(number, Quaternion):
            return number
        else:
            return Quaternion([number.real, number.imag, 0, 0])

    @property
    def real(self):
        return self._real

    @real.setter
    def real(self, value):
        # TODO: add check to make sure it is valid
        self._real = value
    
    @property
    def imag(self):
        return self._imag

    @imag.setter
    def imag(self, value):
        # TODO: add check to make sure it is valid
        self._imag = value

    @property
    def imaginary(self):
        self._imaginary = self.vector[1:]
        return self._imaginary

    @imaginary.setter
    def imaginary(self, value):
        self._imaginary = value

    @property
    def imagNorm(self):
        self._imagNorm = self._imaginary.dot(self._imaginary)
        return self._imagNorm

    @imagNorm.setter
    def imagNorm(self, value):
        # TODO: add check to make sure it is valid
        # this doesn't feel like the best way to do this
        self._imagNorm = value

    @property
    def norm(self):
        self._norm = self.vector.dot(self.vector)
        return self.norm

    @norm.setter
    def norm(self, value):
        self._norm = value

    def conjugate(self):
        return Quaternion([self.real, -self.imag, -self.j, -self.k])

    # TODO makes this return an array from which quaternion could be constructed
    def inverse(self):
        return Quaternion(self.conjugate().vector / self.norm())

    def __eq__(self, other):
        if isinstance(self, Quaternion):
            if isinstance(other, Quaternion):
                return np.array_equal(self.vector, other.vector)
            elif isinstance(other, (numbers.Number, np.signedinteger, np.floating)):
                return np.array_equal(self.vector, np.array((other, 0, 0, 0)))
        return False

    def __complex__(self):
        return complex(self.real, self.imag)

    def __neg__(self):
        return Quaternion(-self.vector)

    def __pos__(self):
        return self

    def __abs__(self):
        # TODO replace with radical class once implemented
        return np.sqrt(self.norm)

    def __repr__(self):
        # TODO make this not shit
        # this is a really lazy representation
        # consider removing coefficient if it is ==1
        # don't show component if corresponding coefficient ==0
        # make it so negative coefficients display as - instead of +-
        return str(self.real) + '+' + str(self.imag) + 'i' + '+' + str(self.j) + 'j' + '+' + str(self.k) + 'k'

    def __add__(self, other):
        if isinstance(other, (numbers.Real, np.signedinteger, np.floating)):
            return Quaternion(self.vector + np.array([other, 0, 0, 0]))
        elif isinstance(other, Quaternion):
            return Quaternion(self.vector + other.vector)
        elif isinstance(other, numbers.Complex):
            return Quaternion(self.vector + np.array([other.real, other.imag, 0, 0]))
        else:
            raise NotImplementedError

    def __radd__(self, other):
        return self * other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return self + (-other)

    def _mul_i(self):
        return np.array((-self.imag, self.real, self.k, -self.j))

    def _mul_j(self):
        return np.array((-self.j, -self.k, self.real, self.imag))

    def _mul_k(self):
        return np.array((-self.k, self.j, -self.imag, self.real))

    def __mul__(self, other):
        if isinstance(other, (numbers.Real, np.signedinteger, np.floating)):
            return Quaternion(other * self.vector)
        elif isinstance(other, Quaternion):
            return (Quaternion(self.vector * other.real + 
                               self._mul_i() * other.imag +
                               self._mul_j() * other.j +
                               self._mul_k()*other.k))
        elif isinstance(other, numbers.Complex):
            return (Quaternion(self.vector * other.real +
                               self._mul_i() * other.imag))
        else:
            raise NotImplementedError

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, (numbers.Real, np.signedinteger, np.floating)):
            return Quaternion(self.vector / other)
        elif isinstance(other, Quaternion):
            return self * other.inverse()
        elif isinstance(other, numbers.Complex):
            # this feels like a bad way of handling
            return self / Quaternion([other.real, other.imag, 0, 0])
        else:
            raise NotImplementedError

    def __rtruediv__(self, other):
        return self * other
    
    def __div__(self, other):
        return self.__truediv__(other)
    
    def __rdiv__(self, other):
        return other.__truediv__(self)
    
    def __pow__(self, exponent):
        # does this work with complex numbers?
        if isinstance(exponent, (numbers.Real, np.signedinteger, np.floating)):
            magnitude = abs(self) ** exponent
            angle = self.real / abs(self)
            unitVector = self.imaginary / np.sqrt(self.imagNorm) * abs(self)
            angle *= exponent
            # possibly write my own trig functions
            return magnitude * Quaternion(np.pad(unitVector * np.sin(angle),
                                          (1, 0), constant_values=(np.cos(angle), 0)))
        else:
            raise NotImplementedError

    def __rpow__(self, base):
        # does this work with complex numbers?
        if isinstance(base, (numbers.Real, np.signedinteger, np.floating)):
            magnitude = base ** self.real
            log = np.log(base)
            angle = log * self.imagNorm
            return magnitude * Quaternion(np.pad(self.imaginary / self.imagNorm * np.sin(angle),
                                          (1, 0), constant_values=(np.cos(angle), 0)))

    def __hash__(self):
        return hash(self.vector)

    def __len__(self):
        return 4