import numpy as np
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        array = np.asarray(nums)
        for i,e in enumerate(nums):
            true_false_array = array[i+1:] + e == target
            if true_false_array.any():
                aa = np.where(true_false_array == True)
                return [i,aa[0][0]+(i+1)]

aaa = Solution()
print(aaa)
print(aaa.twoSum([3,2,4,0], 3))
