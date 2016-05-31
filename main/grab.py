from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import codecs

class grab:
	"""grab dynamic page"""
	url = ""
	page_tree_str = ""

	def __init__(self, URL):
		self.url = URL

	def get_dynamic_content(self, path):
		# Start the WebDriver and load the page
		wd = webdriver.Firefox()
		wd.get(self.url)
		wd.implicitly_wait(5)
		path = "../files/"+ path
		fo1 = codecs.open(path, "w+", "utf-8")
		page_tree_str = wd.page_source
		fo1.write(page_tree_str)
		fo1.close()
		return page_tree_str

