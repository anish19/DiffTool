from bs4 import BeautifulSoup, NavigableString, Tag


class PageTree(object):
	"""docstring for PageTree"""
	url = ''
	soup = ''
	max_level = -1
	id_ctr = 1

	def __init__(self, page, parser='lxml'):
		self.soup = BeautifulSoup(page, parser)

	def build_tree(self):
		pass

	def save_html(self):
		new_file = open(self.name + str(self.version), "w")
		self.version = self.version + 1
		new_file.write(str(self.soup))
