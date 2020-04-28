import requests
from bs4 import BeautifulSoup
import json

'''
代码思路：
	1.利用requests去获取网站上面的数据（前端源代码），在源代码中有我们想要的数据
	2.在源代码中筛选出我们想要的数据，用bs4
	3.把筛选出来的数据存放到文件中
'''

# 请求头 定义一个伪造的浏览器
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/81.0.4044.122 Safari/537.36 Edg/81.0.416.64'}

# 利用requests获取数据
def getPage(url):
	# 异常处理 保证程序不会因为断网等一系列原因崩溃
	try:
		response = requests.get(url, headers = headers)
		if response.status_code == 200:
			return response.text
		else:
			return None
	except Exception:
		return None

# url = 'https://maoyan.com/'
# print(getPage(url))

# 获取电影信息
def getInfo(html):
	# 使用 BeautifulSoup 匹配电影的排名、海报、电影名、主演以及评分
	# BeautifulSoup() 必须传入两个参数：你要提取的网页 和 html解析器
	soup = BeautifulSoup(html, 'lxml') # BS本身是选择器
	# 找到网页中所有dd标签
	items = soup.select('dd')

	for item in items:
		index = item.find('i', class_ = 'board-index').get_text()
		name = item.find('p', class_ = 'name').get_text()
		star = item.find('p', class_ = 'star').get_text().strip()[3:]
		time = item.find('p', class_ = 'releasetime').get_text()[5:]
		score = item.find('p', class_ = 'score').get_text()

		# 用生成器去返回
		yield {
				'排名': index,
				'电影名称': name,
				'主演': star,
				'上映时间': time,
				'评分': score
				}

# 写入文件
def writeFile(file):
	with open('E:\\All_Test_Files\\Py_File\\猫眼电影排行榜数据.txt', 'a', encoding = 'utf-8') as f:
		# 在python中，一个对象无法写入文件中，所以要把字典对象转成json数据
		f.write(json.dumps(file, ensure_ascii = False) + '\n')

# 程序入口
if __name__ == "__main__":
	for num in [i * 10 for i in range(11)]:
		url = 'https://maoyan.com/board/4?offset=' + str(num)
		html = getPage(url)

		for item in getInfo(html):
			print(item)
			writeFile(item)
