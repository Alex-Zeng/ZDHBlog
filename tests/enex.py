class EnterExitDemo(object):
    def __init__(self, str):
        self.str = str

    def __enter__(self):
        print('enter')
        self.str += '-->enter'
        return self.str

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')
        self.str += '-->exit'



with EnterExitDemo('道可道非常道') as f:
    print(f)