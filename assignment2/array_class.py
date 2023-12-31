"""
Array class for assignment 2
"""
import math

class Array:

    def __init__(self, shape, *values):
        """
        checks if given args consitiute a valid array
        Array(shape, val1, val2, .....)
        Vals can either be of type bool, int or float and the array has to be
        homogenus, meaning only containing one type
        shape has to be tuple containing the
        """
        """
        n-d array
        """
        if not all([isinstance(d, int) for d in shape]) or not isinstance(shape, tuple):
            raise TypeError('shape has to be tuple with ints as args')
        if not isinstance(values[0], (int, float, bool)):
            raise TypeError('values can only be of types int, float and bool')
        if not all([isinstance(val, type(values[0])) for val in values]):
            raise TypeError('All values need to be of same type, either int, float or bool')
        if math.prod(shape) != len(values):
            raise ValueError("nr of vals don't match shape")

        def self_values_maker(values, shape):
            if len(shape) == 1:
                return values
            nr_nests = shape[0]
            nr_vals_in_nest = len(values)/nr_nests
            for n in range(nr_nests):
                values[n] = values[int(n*nr_vals_in_nest):int((n+1)*nr_vals_in_nest)]
            return [self_values_maker(values[i], shape[1:]) for i in range(nr_nests)]
        self.values   = values
        self.values_print = self_values_maker(list(values), shape)
        self.shape  = shape

    def __str__(self):
        return f'{self.values_print}'
    def __getitem__(self,key):
        """ Gets item with given key/index"""
        return self.values[key]


    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        if isinstance(self.values[0], bool):
            return NotImplemented
        if isinstance(other, (float,int)):
            new_vals = [other + e for e in self.values]
            return Array(self.shape, *new_vals)

        if isinstance(other, Array):
            if isinstance(other.values[0], bool) or self.shape != other.shape:
                return NotImplemented
            new_vals = [e1 + e2 for e1, e2 in zip(self.values, other.values)]
            return Array(self.shape, *new_vals)

        return NotImplemented

    def __radd__(self, other):
        """
            same as __add__

            kicks in if other is not an Array. If we let A be an Array and let python run
            1 + A it will look for 1's (a int) special method for Adding. Since python
            doesn't have my class Array implemented it won't find anything. Therfore we
            just swap the order of the opperands, to A + 1 so that we use our __add__

        """
        return self.__add__(other)

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """

        return self.__add__(other.__mul__(-1))


    def __rsub__(self, other):
        """
        same as __sub__

        see __radd__ for further info
        """
        return (-1*self).__sub__(-1*other)

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        if isinstance(other, Array):
            if isinstance(other.values[0], bool) or isinstance(self.values[0], bool) \
            or self.shape != other.shape:
                return NotImplemented
            new_vals = [e1*e2 for e1,e2 in zip(self.values, other.values)]
            return Array(self.shape, *new_vals)
        if isinstance(other, int) or isinstance(other,float):
            new_vals = [other * e for e in self.values]
            return Array(self.shape, *new_vals)
        return NotImplemented
    def __rmul__(self, other):
        """
        same as __mul__

        see __radd__ for more information
        """
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        if not isinstance(other, Array) or self.shape != other.shape:
            return False
        else:
            for elm1, elm2 in zip(self.values, other.values):
                if not math.isclose(elm1,elm2):
                    return False
            return True

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it should return TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """

        if isinstance(other, Array):
            if other.shape != self.shape:
                raise ValueError
            new_vals = [math.isclose(e1,e2) for e1,e2 in zip(self.values, other.values)]
            return Array(self.shape, *new_vals)

        if isinstance(other, bool) or isinstance(other, int) or isinstance(other, float):
            new_vals = [math.isclose(other, e) for e in self.values]
            return Array(self.shape, *new_vals)

        raise TypeError

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.

        """

        if isinstance(self.values[0], bool):
            raise TypeError
        smallest = self.values[0]
        for elm in self.values:
            if elm < smallest:
                smallest = elm
        return smallest

    def mean_element(self):
        """Returns the mean value of an array

        Only needs to work for type int and float (not boolean).

        Returns:
            float: the mean value
        """
        if isinstance(self.values[0], bool):
            raise TypeError
        return sum(self.values)/len(self.values)
