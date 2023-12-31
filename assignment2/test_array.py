"""
Tests for our array class
"""

from array_class import Array
import math
import pytest


shape = (3,)
my_array = Array(shape, 2, 3, 1)
my_other_array = Array((3,), 2.3, 4.2, 3.2)
da_bool = Array((2,), False, True)

def test_str_1d():
    assert str(my_array) == '[2, 3, 1]'
    assert str(my_other_array) == '[2.3, 4.2, 3.2]'

@pytest.mark.parametrize('arg1, arg2, output', [(my_array, my_other_array, Array((3,), 2+ 2.3, 3 + 4.2, 1 + 3.2)), \
(my_other_array, 2, Array((3,), 4.3, 6.2, 5.2)), (2.7, my_array, Array((3,), 2+ 2.7, 3 + 2.7, 1 + 2.7))])
def test_add_1d(arg1, arg2, output):
    assert (arg1+arg2 == output)
    with pytest.raises(TypeError):
        da_bool + 2

arr   = Array((2,), 3, 4)
arr_f = Array((2,), 1.3, 9.44)
"""
made some shorter arrays for less pain
"""

@pytest.mark.parametrize('arg1, arg2, output', [(arr, arr_f, Array((2,), 3- 1.3, 4 - 9.44)), \
(arr_f, 2, Array((2,), 1.3-2, 9.44-2)), (2.7, arr_f, Array((2,), 2.7-1.3, 2.7-9.44))])
def test_sub_1d(arg1, arg2, output):
    assert arg1 - arg2 == output
    with pytest.raises(TypeError):
        da_bool - 199

@pytest.mark.parametrize('arg1, arg2, output', [(my_array, my_other_array, Array((3,), 2*2.3, 3*4.2, 1*3.2)), \
(3, my_array, Array((3,), 3*2, 3*3, 3*1 ))])
def test_mul_1d(arg1, arg2, output):
    assert arg1*arg2 == output
    with pytest.raises(TypeError):
        da_bool * 'frog'


def test_eq_1d():
    assert my_array == my_array
    assert not(my_array == my_other_array)
    assert not(my_array == 'frog')

my_other_array2 = Array((3,), 2.00, 3.3, 0.0)
@pytest.mark.parametrize('arg1, arg2, output', [(my_array, my_other_array, Array((3,), False, False, False)), \
(my_other_array2, my_array, Array((3,), True, False, False)), (da_bool, False, Array((2,), True, False))])
def test_same_1d(arg1, arg2, output):
    assert arg1.is_equal(arg2) == output

def test_smallest_1d():
    assert my_array.min_element() == 1
    assert my_other_array.min_element() == 2.3
    def type_error_test():
        try:
            da_bool.min_element()
        except TypeError:
            return True
    assert type_error_test()



def test_mean_1d():
    assert math.isclose(my_array.mean_element(), (2+3+1)/3)
    def type_error_test():
        try:
            da_bool.mean_element()
        except TypeError:
            return True
    assert type_error_test()

# 2D tests (Task 6)

my_2d_arr = Array((3,2),1,2,3,4,5,6)
my_other_2d_arr = Array((3,2), 45, 2, 1, 5, 3, 4)
my_third_2d_arr = Array((2,6), 3,4,1,1,3,5,2,56,4,6,3,5)

@pytest.mark.parametrize('arg1, arg2, output', [(my_2d_arr, my_other_2d_arr, \
Array((3,2), 1+45, 2+2, 3+1, 4+5, 5+3, 6+4)), (2, my_2d_arr, Array((3,2), 3,4,5,6,7,8))])
def test_add_2d(arg1, arg2, output):
    assert arg1 + arg2 == output


@pytest.mark.parametrize('arg1, arg2, output', [(my_2d_arr, my_other_2d_arr, \
Array((3,2), 1*45, 2*2, 3*1, 4*5, 5*3, 6*4)), (4, my_2d_arr, \
Array((3,2), 4*1, 4*2, 4*3, 4*4, 4*5, 4*6) )])
def test_mult_2d(arg1, arg2, output):
    assert arg1*arg2 == output

@pytest.mark.parametrize('arg1, arg2, output', [(my_2d_arr, my_other_2d_arr, \
Array((3,2), False, True, False, False, False, False))])
def test_same_2d(arg1, arg2, output):
    assert arg1.is_equal(arg2)  == output

@pytest.mark.parametrize('arg1, output', [(my_2d_arr, 7/2), (my_third_2d_arr, 31/4 )])
def test_mean_2d(arg1, output):
    assert math.isclose(arg1.mean_element(), output)


if __name__ == "__main__":
    """
    Note: Write "pytest" in terminal in the same folder as this file is in to run all tests
    (or run them manually by running this file).
    Make sure to have pytest installed (pip install pytest, or install anaconda).
    """

    # Task 4: 1d tests
    test_str_1d()
    test_add_1d()
    test_sub_1d()
    test_mul_1d()
    test_eq_1d()
    test_mean_1d()
    test_same_1d()
    test_smallest_1d()

    # Task 6: 2d tests
    test_add_2d()
    test_mult_2d()
    test_same_2d()
    test_mean_2d()
