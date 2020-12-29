import numpy as np
import math
import numbers

# TODO: add not implemented thing to arithmetic operators
# TODO: reorganize class body

def to_frac(n):
    if type(n) == Frac:
        return n
    # elif type(n)==int or type(n)==np.int32:
    #   return(Frac(n,1))
    return Frac(int(n), 1)

def mod_inverse(value, mod):
    # perform extended euclidean algorithm to ensure gcd == 1 and find modular inverse
    prevRemainder = mod
    remainder = value % mod
    # coefficients such that bezout1*mod + bezout2*(self.denominator % mod) = remainder
    # satisfying bezouts equation
    prevBezout1 = 1
    bezout1 = 0
    prevBezout2 = 0
    bezout2 = 1
    # algorithm stops when remainder which is non negative reaches 0
    while remainder:
        quotient = prevRemainder // remainder
        prevRemainder, remainder = remainder, prevRemainder - quotient * remainder
        prevBezout1, bezout1 = bezout1, prevBezout1 - quotient * bezout1
        prevBezout2, bezout2 = bezout2, prevBezout2 - quotient * bezout2
    return prevBezout2, prevRemainder


integralTypes = (int, np.signedinteger, numbers.Integral)
floatTypes = (float, numbers.Real, np.floating)

class Frac(numbers.Rational):

    __slots__ = ('_numerator', '_denominator')

    def __round__(self, ndigits=None):
        return round(self.value(), ndigits)

    def __mod__(self, mod):
        if isinstance(mod, integralTypes):
            mod = abs(mod)
            inverse, gcd = mod_inverse(self.denominator, mod)
            if gcd != 1:
                # TODO: make error message better
                raise NotImplementedError("modular inverse not able to be calculated")
            return (inverse * self.numerator) % mod
        raise NotImplementedError("Mod must be integral")

    def __rmod__(self, other):
        raise NotImplementedError("Fractions may not be modulus")

    def __abs__(self):
        return Frac(abs(self.numerator), abs(self.denominator))

    def __rfloordiv__(self, other):
        return math.floor(self / other)

    def __floordiv__(self, other):
        return math.floor(self / other)

    def __ceil__(self) -> int:
        return np.ceil(self.value())

    def __floor__(self) -> int:
        return np.floor(self.value())

    def __trunc__(self) -> int:
        value = self.value()
        if value >= 0:
            return np.floor(value)
        else:
            return -np.floor(-value)

    def __init__(self, numerator=1, denominator=1):
        if denominator == 0:
            raise ZeroDivisionError
        self._numerator = numerator.numerator * denominator.denominator
        self._denominator = numerator.denominator * denominator.numerator
        self.reduce()

    @property
    def numerator(self):
        return self._numerator

    @numerator.setter
    def numerator(self, value):
        if isinstance(value, integralTypes):
            self._numerator = value
        else:
            raise ValueError("numerator must be int")

    @property
    def denominator(self):
        return self._denominator

    @denominator.setter
    def denominator(self, value):
        if isinstance(value, integralTypes):
            self._denominator = value
        else:
            raise ValueError("denominator must be int")

    def reduce(self):
        m = math.gcd(self.numerator, self.denominator)
        self.numerator = self.numerator // m
        self.denominator = self.denominator // m

    def inv(self):
        return Frac(self.denominator, self.numerator)

    def __add__(self, other):
        if isinstance(other, integralTypes):
            numerator = self.numerator * other.denominator + self.denominator * other.numerator
            denominator = self.denominator * other.denominator
            return Frac(numerator, denominator).reduce()
        elif isinstance(other, floatTypes):
            return other * self.value()

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return Frac(-self.numerator, self.denominator)

    def __sub__(self, n):
        return self + (-n)

    def __rsub__(self, n):
        return self + (-n)

    def __mul__(self, other):
        if isinstance(other, integralTypes):
            return Frac(self.numerator * other.numerator, self.denominator * other.denominator)
        elif isinstance(other, floatTypes):
            return self.value() * other

    def __rmul__(self, n):
        return self * n

    def __truediv__(self, n):
        n = to_frac(n)
        return self * Frac.inv(n)

    def __rtruediv__(self, n):
        n = to_frac(n)
        return self.inv() * n

    def __pow__(self, power):
        # TODO make radical class and make this work for that
        if isinstance(power, integralTypes):
            if power == 0:
                return Frac()
            elif power > 0:
                return Frac(self.numerator ** power, self.denominator ** power)
            else:
                return Frac(self.denominator ** (-power), self.numerator ** (-power))

    def __rpow__(self, base):
        # TODO: something with radicals
        raise NotImplementedError("Noah add radicals")

    def __eq__(self, other):
        if isinstance(other, integralTypes):
            return self.numerator * other.denominator == self.denominator * other.numerator
        elif isinstance(other, floatTypes):
            return other * self.denominator / self.numerator == 1

    def __lt__(self, other):
        if isinstance(other, integralTypes):
            return self.numerator * other.denominator < self.denominator * other.numerator
        elif isinstance(other, floatTypes):
            return self.value() < other

    def __le__(self, other):
        return self < other or self == other

    def __pos__(self):
        return self

    def value(self):
        return self.numerator / self.denominator

    def __repr__(self):
        if self.denominator == 1:
            return str(self.numerator)
        return str(self.numerator) + '/' + str(self.denominator)

    def __hash__(self) -> int:
        return hash((self.numerator, self.denominator))

    def __int__(self) -> int:
        return int(self.value())