from bs4 import BeautifulSoup, NavigableString, Tag
import urllib2


class PageTree2():
    """docstring for PageTree2"""
    url = ''
    soup = ''
    max_level = -1
    id_ctr = 1

    def __init__(self, page, parser='lxml'):
        self.soup = BeautifulSoup(page, parser)

    def __add_levels(self, tree, level, offset, ctr_flag):
        # tree['value_z1z'] = ""
        if (level > self.max_level):
            self.max_level = level
        for child in tree.children:
            if (not isinstance(child, NavigableString)):
                # child['match'] = 0
                child['level'] = level + 1 + offset;
                if ctr_flag == 1:
                    child['id_diff_z1z'] = self.id_ctr
                child['isDiff'] = 0
                self.id_ctr += 1
                # tree['value_z1z'] += child.name + " "
                self.__add_levels(child, level + 1, offset, ctr_flag)

    def get_max_level(self):
        return self.max_level

    def build_tree(self):
        self.soup.html['level'] = 0
        self.soup.html['match'] = 0
        self.soup.html['id_diff_z1z'] = 0
        self.__add_levels(self.soup.html, 0, -1, 0)
        for tag in self.soup.find_all(True):
            if (tag.has_attr('level')):
                tag['hash'] = hash(tag)
        self.id_ctr = 0
        self.__add_levels(self.soup.html, 0, 0, 1)

    def save_html(self):
        new_file = open(self.name + str(self.version), "w")
        self.version = self.version + 1
        new_file.write(str(self.soup))
