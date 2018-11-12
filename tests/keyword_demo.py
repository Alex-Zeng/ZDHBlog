class Solution:
    def maxProfit(self, prices):
        """
        买卖股票的最佳时机 II
        给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。
        设计一个算法来计算你所能获取的最大利润。你可以尽可能地完成更多的交易（多次买卖一支股票）。
        注意：你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。
        :type prices: List[int]
        :rtype: int
        """
        p_len = len(prices)
        if p_len < 2:
            return 0

        profit = 0

        i = 0
        while i < p_len - 1:
            if prices[i + 1] > prices[i]:
                profit += prices[i + 1] - prices[i]
            i += 1

        return profit

    def removeDuplicates(self, nums):
        """
        从排序数组中删除重复项
        给定一个排序数组，你需要在原地删除重复出现的元素，使得每个元素只出现一次，返回移除后数组的新长度。
        不要使用额外的数组空间，你必须在原地修改输入数组并在使用 O(1) 额外空间的条件下完成。
        :type nums: List[int]
        :rtype: int
        """
        for i in range(len(nums) - 1, -1, -1):
            if nums[i] == nums[i - 1]:
                nums.remove(nums[i])
        return len(nums)


    def rotate(self, nums, k):
        """旋转数组
        给定一个数组，将数组中的元素向右移动 k 个位置，其中 k 是非负数。
        :type nums: List[int]
        :type k: int
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        #解法一 效率低
        # for i in range(k):
        #     nums.insert(0,nums.pop())

        #解放二 切片
        nums_len = len(nums)
        i = k % nums_len
        print(i)
        n1 = nums[:nums_len - i]
        n2 = nums[-i:]
        nums[:i] = n2
        nums[i:] = n1

    def containsDuplicate(self, nums):
        """存在重复元素
        给定一个整数数组，判断是否存在重复元素。
        如果任何值在数组中出现至少两次，函数返回 true。如果数组中每个元素都不相同，则返回 false
        :type nums: List[int]
        :rtype: bool
        """
        if (len(set(nums)) == len(nums)):
            return False
        else:
            return True

    def intersect(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        

        tmp = [val for val in nums1 if val in nums2]

        return tmp

if __name__ == '__main__':
    cal = Solution()
    ss = [0,1, 1,5,5]
    nums1 = [1, 2, 2, 1]
    nums2 = [2,3,4]
    # set_l = cal.maxProfit(ss)
    cal.containsDuplicate(ss)
    print(cal.intersect(nums1,nums2))
