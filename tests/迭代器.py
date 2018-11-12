'''
迭代器
迭代是Python最强大的功能之一，是访问集合元素的一种方式。

迭代器是一个可以记住遍历的位置的对象。

迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退。

迭代器有两个基本的方法：iter() 和 next()。

字符串，列表或元组对象都可用于创建迭代器：
'''

class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        x = self.a
        self.a += 1
        if x > 10:
            raise StopIteration
        return x

def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

if __name__ == '__main__':
    # myclass = MyNumbers()
    # myiter = iter(myclass)
    # it = iter(myiter)  # 创建迭代器对象
    # while True:
    #     print(next(it)) # 输出迭代器的下一个元素

    print(list(frange(0, 1, 0.125)))