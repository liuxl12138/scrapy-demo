from scrapy import cmdline
import datetime

#cmdline.execute("scrapy crawl jobspider".split())

# 当前时间字符串
now_date_str = datetime.datetime.now().strftime("%m-%d")
# 当前时间
now_date = datetime.datetime.strptime(now_date_str, '%m-%d')
pub_date = datetime.datetime.strptime('6-12', '%m-%d')
print((now_date - pub_date).days)

