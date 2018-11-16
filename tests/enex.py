#encoding:utf8
#url安全序列化
#防篡改
#明文加密传输
#更多相关知识请看https://itsdangerous.readthedocs.io/en/latest/
from itsdangerous import URLSafeSerializer
s = URLSafeSerializer('secret-key')
print (s.dumps([1, 2, 3, 4]))
#WzEsMiwzLDRd.wSPHqC0gR7VUqivlSukJ0IeTDgo
print (s.loads('WzEsMiwzLDRd.wSPHqC0gR7VUqivlSukJ0IeTDgo'))
