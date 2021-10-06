#md5进行数据的加密
import hashlib
#md5加密
def Encrypt(str):
    m = hashlib.md5()  #创建一个hashlib.md5()对象
    m.update(str.encode("utf8"))    #将参数转换为UTF8编码
    return m.hexdigest().upper()        #用十六进制输出加密后的数据
 