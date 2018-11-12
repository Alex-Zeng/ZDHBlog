# !/usr/bin/python3

# 输入阿拉伯数字金额,转换成大写金额

class TransNumber:
    switch = {
        '0': '零',
        '1': '壹',
        '2': '贰',
        '3': '叁',
        '4': '肆',
        '5': '伍',
        '6': '陆',
        '7': '柒',
        '8': '捌',
        '9': '玖',
    }

    def trans(self, num):
        print(type(num))
        # 先分离整数和小数位
        num_l = str(num).split('.')
        final_num = []
        if len(num_l[0]) > 13:
            return '数值过大无法计算'
        elif not num_l[0].isdigit():
            return '参数无效'

        # 判断小数位前两位(角分)
        if len(num_l) == 2:
            for i, val in enumerate(num_l[1]):
                c_val = self.switch[str(val)]
                if c_val != '零':
                    if i == 0:
                        c_val += '角'
                        final_num.append(c_val)
                    elif i == 1:
                        c_val += '分'
                        final_num.append(c_val)
        # 转换正整数
        for k, val_z in enumerate(reversed(num_l[0])):
            cz_val = self.switch[str(val_z)]
            if k == 4 and cz_val == '零':
                cz_val = '万'
            elif k == 4:
                cz_val += '万'
            elif k == 8 and cz_val == '零':
                cz_val = '亿'
            elif k == 8:
                cz_val += '亿'

            if cz_val != '零':
                if k == 0:
                    cz_val += '圆'
                elif k == 1:
                    cz_val += '拾'
                elif k == 2:
                    cz_val += '佰'
                elif k == 3:
                    cz_val += '仟'
                elif k == 5:
                    cz_val += '拾'
                elif k == 6:
                    cz_val += '佰'
                elif k == 7:
                    cz_val += '仟'
                elif k == 9:
                    cz_val += '拾'
                elif k == 10:
                    cz_val += '佰'
                elif k == 11:
                    cz_val += '仟'
                elif k == 12:
                    cz_val += '万'
                elif k == 13:
                    cz_val += '亿'
            final_num.insert(0, cz_val)

        # 拼接字符串,消除多余的零
        final_str = ''.join(final_num)
        while final_str.find('零零') != -1:
            final_str = final_str.replace('零零', '零')

        return final_str.rstrip('零')


if __name__ == '__main__':
    tran = TransNumber();
    print(tran.trans(22-22))
