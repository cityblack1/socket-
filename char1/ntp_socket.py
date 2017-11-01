"""
其实就是先创建一个实例，连接到一个指定的网站pool.ntp.org
然后向他发送请求，得到响应
"""
import ntplib
from time import ctime

def print_time():
    # ctime 将一个1970（epoch）后的秒字符串转化为本地时间的字符串
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('pool.ntp.org')
    print(ctime(response.tx_time))
    """
    正常情况下：
    $ python 1_11_print_machine_time.py
    Thu Mar 5 14:02:58 2012
    但是：
    在中国无法访问pool.ntp.org
    所以无法得到响应
    """


if __name__ == "__main__":
    print_time()