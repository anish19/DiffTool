import pagetree
from bs4 import BeautifulSoup, NavigableString, Tag
import codecs

class PageTreeDiff(object):
	''''''
	ref_tree = ''
	comp_tree = ''
	ref_count = 0
	comp_count = 0
	ref_map = {}    #dict of all element hash of ref tree
	comp_map = {}   #dict of all element hash of comp tree
	ref_id_ele_map = {}
	comp_id_ele_map = {}
	comp_max_level = 0
	ref_max_level = 0
	diff_hash_list = [] #list of diff hashes between ref_map and comp_map
	diff_id_list = []   #list of diff ids between ref_map and comp_map
	folder = ""

	def __init__(self,ref_tree,ref_max_level,comp_tree,comp_max_level,folder ):
		self.ref_tree = ref_tree
		self.ref_max_level = ref_max_level
		self.comp_tree = comp_tree
		self.comp_max_level = comp_max_level
		self.__build_ref_tree(ref_tree)
		self.__build_comp_tree(comp_tree)
		self.folder = folder

	def __build_ref_tree(self, tree):
		if not isinstance(tree, NavigableString):
			for child in tree.children:
				if len(child) > 0:
					# print "----"
					if not isinstance(child, NavigableString):
						self.ref_map[child['id_diff_z1z']] = child['hash']
						self.ref_id_ele_map[child['id_diff_z1z']] = child
						self.ref_count += 1
					# print child
					# print "====="
					self.__build_ref_tree(child)
		else:
			return

	def print_ref_map(self):
		print "ref hash list size : ", len(self.ref_map.items())
		print self.ref_map.items()

	def __build_comp_tree(self, tree):
		if not isinstance(tree, NavigableString):
			for child in tree.children:
				if len(child) > 0:
					if not isinstance(child, NavigableString):
						self.comp_map[child['id_diff_z1z']] = child['hash']
						self.comp_id_ele_map[child['id_diff_z1z']] = child
						self.comp_count += 1
					self.__build_comp_tree(child)

	def print_comp_map(self):
		print "comp hash list size : ", len(self.comp_map.items())
		print self.comp_map.items()

	def find_diff(self):
		for key, value in self.comp_map.iteritems():
			if value not in self.ref_map.values():
				self.diff_hash_list.append(value)
				self.diff_id_list.append(key)
		if len(self.diff_hash_list) == 0:
			print "No difference between two trees"
			return
		else:
			print "Difference exists between two trees"
			#print self.diff_hash_list
			#print self.diff_id_list
			ref_file = codecs.open("../files/"+self.folder+"ref_tree.html", "w+", "UTF-8")
			comp_file = codecs.open("../files/"+self.folder+"comp_tree.html", "w+", "UTF-8")
			ref_file.write(self.ref_tree.prettify())
			comp_file.write(self.comp_tree.prettify())
			ref_file.close()
			comp_file.close()

			diff_id_ele_list = []
			for id in self.diff_id_list:
				id_ele = id, self.comp_id_ele_map[id]
				diff_id_ele_list.append(id_ele)
			return diff_id_ele_list
			#self.__find_tag(self.ref_tree, self.comp_tree)

	def __find_tag(self, ref_tree, comp_tree):
		ref_tree_size = len(ref_tree.contents)
		ref_tree['child-num'] = ref_tree_size
		comp_tree_size = len(comp_tree.contents)
		comp_tree['ref-child-num'] = ref_tree_size
		comp_tree['child-num'] = comp_tree_size
		if(ref_tree_size != comp_tree_size):
			self.__mark_diff(ref_tree, ref_tree_size, comp_tree, comp_tree_size)
			return
		else:
			for i in xrange(0, ref_tree_size):
				if not isinstance(ref_tree.contents[i], NavigableString) and not isinstance(comp_tree.contents[i], NavigableString):
					if ref_tree.contents[i]['hash'] == comp_tree.contents[i]['hash']:
						comp_tree.contents[i]['match'] = 1
						self.__add_style(comp_tree.contents[i], "background-color:rgba(0,191,255,1.0);")
					else:
						comp_tree.contents[i]['match'] = -1
						self.__find_tag(ref_tree.contents[i], comp_tree.contents[i])

	def __mark_diff(self, ref, rsize, comp, csize):
		ref_child_hash_list = []
		comp_child_hash_list = []
		for comp_child in comp.children:
			if not isinstance(comp_child, NavigableString):
				comp_child_hash_list.append(comp_child['hash'])
		for ref_child in ref.children:
			if not isinstance(ref_child, NavigableString):
				ref_child_hash_list.append(ref_child['hash'])

		for child in comp.children:
			if not isinstance(child, NavigableString):
				if child['hash'] not in ref_child_hash_list:
					child['match'] = -1
				#	self.__add_style(child, "background-color:rgba(220,20,60,0.3);")
				else:
					child['match'] = 1

	def __add_style(self, item, style):
		if item.has_attr('style'):
			item['style'] = item['style']+ ";" + style
		else:
			item['style'] = style

	def print_tree(self, tree):
		if not isinstance(tree, NavigableString):
			for child in tree.children:
				if len(child) > 0:
					if not isinstance(child, NavigableString):
						print '___'
						print child
						print '~~~'
						self.print_tree(child)

	def save_comp_tree(self):
		# print self.comp_tree.prettify()
		file = open("diffprint.html", "w+")
		str = self.comp_tree.prettify().encode('utf-8')
		# print str
		file.write(str)
		file.close()


