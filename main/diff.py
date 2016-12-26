from bs4 import BeautifulSoup, NavigableString, Tag, Comment
import codecs



class PageTreeDiff(object):
    ''''''

    def __init__(self, ref_tree, comp_tree, folder):
        self.ref_tree = ref_tree  # ref tree for object
        self.comp_tree = comp_tree  #comp tree for object
        self.ctr = 0    #counter to count number of elements

        self.ref_hash_ele_map = {}  # map b/w hash of ref element and element
        self.comp_hash_ele_map = {}  # map b/w hash of comp element and element

        self.ref_hash_id_map = {}   # map b/w hash of ref element and element id
        self.comp_hash_id_map = {}  # map b/w hash of ref element and element id

        self.ref_id_hash_map = {}   # map b/w element id and hash of ref element
        self.comp_id_hash_map = {}  # map b/w element id and hash of ref element

        self.ref_hash_ele_str_map = {}  # map b/w hash of ref element and partial element
        self.comp_hash_ele_str_map = {}  # map b/w hash of comp element and partial element

        self.diff_ele_hash_list = []    #list to store hash of different elements
        self.corresponding_ele_hash_set = set() #partially matching parents set
        self.corresponding_ele_hash_map = {} #partially matching parents map
        self.diff_attr_pair_hash_list = []  #list of corresponding elements in pairs, that have
                                            #different attributes

        self.__build_tree(ref_tree, "ref", "1")
        self.__build_tree(comp_tree, "comp", "1")
        self.folder = folder
        self.diff_ele_list = []
        self.diff_attr_list = set()
        self.oup = 0

    def __build_tree(self, tree, ele_type, id):

        child_ctr = 0
        if not isinstance(tree, NavigableString) and not isinstance(tree, Comment):
            for child in tree.children:
                child_ctr += 1
                self.ctr += 1
                hash_key = hash(child)
                str_child = child.encode('utf-8').strip()
                str_child = (str_child[:75] + '...') if len(str_child) > 75 else str_child

                if ele_type == "ref":
                    self.ref_hash_ele_map[hash_key] = child
                    self.ref_hash_ele_str_map[hash_key] = str_child
                    new_id = id + '.' + str(child_ctr)
                    self.ref_hash_id_map[hash_key] = new_id
                    self.ref_id_hash_map[new_id] = hash_key
                else:
                    self.comp_hash_ele_map[hash_key] = child
                    self.comp_hash_ele_str_map[hash_key] = str_child
                    new_id = id + '.' + str(child_ctr)
                    self.comp_hash_id_map[hash_key] = new_id
                    self.comp_id_hash_map[new_id] = hash_key


                self.__build_tree(child, ele_type, new_id)
        else:
            self.ctr += 1
            hash_key = hash(tree)
            str_tree = tree.encode('utf-8').strip()
            str_tree = (str_tree[:75] + '...') if len(str_tree) > 75 else str_tree
            if ele_type == "ref":
                self.ref_hash_id_map[hash_key] = self.ctr
                self.ref_id_hash_map[self.ctr] = hash_key
                self.ref_hash_ele_map[hash_key] = tree
                self.ref_hash_ele_str_map[hash_key] = str_tree
                self.ref_hash_id_map[hash_key] = id
            else:
                self.comp_hash_id_map[hash_key] = self.ctr
                self.comp_id_hash_map[self.ctr] = hash_key
                self.comp_hash_ele_map[hash_key] = tree
                self.comp_hash_ele_str_map[hash_key] = str_tree
                self.comp_hash_id_map[hash_key] = id


    def find_diff(self, flag):

        oup_file = codecs.open("../files/" + self.folder + "oup.html", "w+", "UTF-8")
        self.oup = oup_file

        self.__find_diff(self.ref_tree.html, self.comp_tree.html)
        self.__find_extra(self.ref_tree.html, self.comp_tree.html)
        self.__add_id(self.ref_tree.html, self.comp_tree.html)

        if flag == 0:
            ref_file = codecs.open("../files/" + self.folder + "ref_tree.html", "w+", "UTF-8")
            comp_file = codecs.open("../files/" + self.folder + "comp_tree.html", "w+", "UTF-8")
        else:
            ref_file = codecs.open("../files/" + self.folder + "ref2_tree.html", "w+", "UTF-8")
            comp_file = codecs.open("../files/" + self.folder + "proxy_tree.html", "w+", "UTF-8")

        ref_file.write(self.ref_tree.prettify())
        comp_file.write(self.comp_tree.prettify())
        ref_file.close()
        comp_file.close()

        oup_file.close()

        return [self.diff_ele_list, self.diff_attr_list]

    def __add_id(self, ref, comp):
        self.__add_ref_id(ref)
        self.__add_comp_id(comp)

    def __add_ref_id(self, tree):
        if not isinstance(tree, NavigableString) and not isinstance(tree, Comment):
            hash_key = hash(tree)
            if hash_key in self.ref_hash_id_map:
                tree['id_z1z0'] = self.ref_hash_id_map[hash_key]
                for child in tree.children:
                    self.__add_ref_id(child)

    def __add_comp_id(self, tree):
        if not isinstance(tree, NavigableString) and not isinstance(tree, Comment):
            hash_key= hash(tree)
            if hash_key in self.comp_hash_id_map:
                tree['id_z1z0'] = self.comp_hash_id_map[hash_key]
                for child in tree.children:
                    self.__add_comp_id(child)

    def __find_extra(self, ref, comp):
        pass


    def __find_diff(self, ref, comp):

        ref_list = []
        comp_list = []
        for child in ref.children:
            ref_list.append(child)
        for child in comp.children:
            comp_list.append(child)

        self.__recursive_diff(ref_list, comp_list)
        self.__create_diff_ele_list()
        # self.__print_diff_ele()
        self.__find_attr_diff()
        self.__create_diff_attr_list()
        # self.__print_diff_attr()

    def __create_diff_attr_list(self):
        for item in self.diff_attr_pair_hash_list:
            if item[0] in self.ref_hash_ele_map:
                ref_entry = self.ref_hash_ele_str_map[item[0]], self.ref_hash_id_map[item[0]]
            if item[1] in self.comp_hash_ele_map:
                comp_entry = self.comp_hash_ele_str_map[item[1]], self.comp_hash_id_map[item[1]]
            self.diff_attr_list.add((ref_entry,comp_entry))


    def __create_diff_ele_list(self):
        diff_ele_list_ref = set()
        diff_ele_list_comp = set()
        for item in self.diff_ele_hash_list:
            if item in self.ref_hash_ele_map:
                diff_ele_list_ref.add((self.ref_hash_ele_str_map[item], self.ref_hash_id_map[item]))
            elif item in self.comp_hash_ele_map:
                diff_ele_list_comp.add((self.comp_hash_ele_str_map[item], self.comp_hash_id_map[item]))
        self.diff_ele_list.append(diff_ele_list_ref)
        self.diff_ele_list.append(diff_ele_list_comp)

    def __print_diff_ele(self):
        for item in self.diff_ele_hash_list:
            print "----------------------------------------------------------------"
            if item in self.ref_hash_ele_map:
                print self.ref_hash_ele_str_map[item]
            elif item in self.comp_hash_ele_map:
                print self.comp_hash_ele_str_map[item]
            else:
                print "oooooooopssss"

    def __print_diff_attr(self):
        for tup in self.diff_attr_pair_hash_list:
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            if tup[0] in self.ref_hash_ele_map:
                print self.ref_hash_ele_str_map[tup[0]]
            print "~~~~~~~~~~~~~~~"
            if tup[1] in self.comp_hash_ele_map:
                print self.comp_hash_ele_str_map[tup[1]]


    def __find_attr_diff(self):
        for ele in self.corresponding_ele_hash_set:
            if ele[0] in self.ref_hash_ele_map and ele[1] in self.comp_hash_ele_map:
                self.__recursive_compare_attr(self.ref_hash_ele_map[ele[0]], self.comp_hash_ele_map[ele[1]])

    def __recursive_compare_attr(self, obj1, obj2):
        if obj1.parent == None or obj2.parent == None:
            return

        tag1 = obj1.encode("UTF-8").strip()
        tag2 = obj2.encode("UTF-8").strip()

        self.corresponding_ele_hash_map[hash(obj1)] = hash(obj2)
        tag1 = tag1[:tag1.find('>')]
        tag2 = tag2[:tag2.find('>')]

        if hash(tag1) != hash(tag2):
            self.diff_attr_pair_hash_list.append((hash(obj1),hash(obj2)))

        self.__recursive_compare_attr(obj1.parent, obj2.parent)

    def __recursive_diff(self, ref, comp):

        ref_hash_list = []
        comp_hash_list = []

        unmatched_ref_hash_list = []    #list of hash of ref elements not present in comp
        unmatched_comp_hash_list = []   #list of hash of comp elements not present in ref

        unmatched_ref_child_hash_list = []      #list of hash  of all children of unmatched ref elements
        unmatched_comp_child_hash_list = []    #list of hash  of all children of unmatched comp elements

        unmatched_ref_unmatched_child_hash_list = []     #list of unmatched ref child in above lists
        unmatched_comp_unmatched_child_hash_list = []     #list of unmatched comp child in above lists

        next_ref_list = []     #list of unmatched children of unmatched ref children with non zero contents
        next_comp_list = []    #list of unmatched children of unmatched comp children with non zero contents

        #creating lists of hash of ref and comp elements
        for ele in ref:
            ref_hash_list.append(hash(ele))
        for ele in comp:
            comp_hash_list.append(hash(ele))

        #creating lists of hash of unmatched ref and comp elements
        for ele in ref_hash_list:
            if ele not in comp_hash_list:
                unmatched_ref_hash_list.append(ele)
        for ele in comp_hash_list:
            if ele not in ref_hash_list:
                unmatched_comp_hash_list.append(ele)

        if len(unmatched_ref_hash_list) == 0 and len(unmatched_comp_hash_list) == 0:
            return

        #creating lists of hash of children of unmatched ref and comp elements
        for ele in unmatched_ref_hash_list:
            for child in self.ref_hash_ele_map[ele].contents:
                unmatched_ref_child_hash_list.append(hash(child))
        for ele in unmatched_comp_hash_list:
            for child in self.comp_hash_ele_map[ele].contents:
                unmatched_comp_child_hash_list.append(hash(child))

        #creating lists of unmatched children from above lists
        found_extra_ref_child = 0
        for ele in unmatched_ref_child_hash_list:
            if ele not in unmatched_comp_child_hash_list:
                unmatched_ref_unmatched_child_hash_list.append(ele)
                found_extra_ref_child += 1
            else:
                self.oup.write("~~~~~~~~~~~~~~~~")
                self.oup.write(str(hash(self.ref_hash_ele_map[ele].parent)))
                self.oup.write(self.ref_hash_ele_map[ele].parent.name)
                # self.oup.write(self.ref_hash_ele_map[ele].parent.text)
                # self.oup.write(str(hash(self.comp_hash_ele_map[ele].parent)))
                # self.oup.write(self.comp_hash_ele_map[ele].parent.text)
                # self.oup.write("~~~~~~~~~~~~~~~~")
                self.corresponding_ele_hash_set.add((hash(self.ref_hash_ele_map[ele].parent), \
                                                     hash(self.comp_hash_ele_map[ele].parent)))

        # print ref
        # for item in unmatched_ref_child_hash_list:
        #     print ">>>>>>>>>"
        #     print item, self.ref_hash_ele_map[item], type(self.ref_hash_ele_map[item])
        #
        # print comp
        # for item in unmatched_comp_child_hash_list:
        #     print "<<<<<<<<<<"
        #     print item, self.comp_hash_ele_map[item], type(self.comp_hash_ele_map[item])

        found_extra_comp_child = 0
        for ele in unmatched_comp_child_hash_list:
            if ele not in unmatched_ref_child_hash_list:
                unmatched_comp_unmatched_child_hash_list.append(ele)
                found_extra_comp_child += 1
            else:
                self.oup.write("~~~~~~~~~~~~~~~~")
                self.oup.write(str(hash(self.ref_hash_ele_map[ele].parent)))
                self.oup.write(self.ref_hash_ele_map[ele].parent.name)
                # self.oup.write(self.ref_hash_ele_map[ele].parent.text)
                # self.oup.write(str(hash(self.comp_hash_ele_map[ele].parent)))
                # self.oup.write(self.comp_hash_ele_map[ele].parent.text)
                # self.oup.write("~~~~~~~~~~~~~~~~")
                self.corresponding_ele_hash_set.add((hash(self.ref_hash_ele_map[ele].parent), \
                                                     hash(self.comp_hash_ele_map[ele].parent)))


        if found_extra_ref_child == 0 and found_extra_comp_child == 0:
            return
        elif found_extra_ref_child == len(unmatched_ref_child_hash_list):
            self.__mark_diff(ref + comp)
            pass

        for ele in unmatched_ref_unmatched_child_hash_list:
            child = self.ref_hash_ele_map[ele]
            if isinstance(child, NavigableString) or isinstance(child, Comment):
                self.__mark_diff([child])
            elif len(child.contents) < 1:
                self.__mark_diff([child])
            elif len(child.contents) == 1:
                self.__mark_diff([child])
                next_ref_list.append(child)
            else:
                next_ref_list.append(child)

        for ele in unmatched_comp_unmatched_child_hash_list:
            child = self.comp_hash_ele_map[ele]
            if isinstance(child, NavigableString) or isinstance(child, Comment):
                self.__mark_diff([child])
            elif len(child.contents) < 1:
                self.__mark_diff([child])
            elif len(child.contents) == 1:
                self.__mark_diff([child])
                next_comp_list.append(child)
            else:
                next_comp_list.append(child)

        if len(next_ref_list) > 0 and len(next_comp_list) > 0:
            self.__recursive_diff(next_ref_list, next_comp_list)
        elif len(next_ref_list) > 0:
            self.__mark_diff(next_ref_list)
        elif len(next_comp_list) > 0:
            self.__mark_diff(next_comp_list)
        else:
            pass


    def __mark_diff(self, diff_list):
        for ele in diff_list:
            self.diff_ele_hash_list.append(hash(ele))

    def print_tree(self, tree):
        if not isinstance(tree, NavigableString):
            for child in tree.children:
                if len(child) > 0:
                    if not isinstance(child, NavigableString):
                        print '___'
                        print child
                        print '~~~'
                        self.print_tree(child)

    def __print_id_ele(self):
        for key,value in self.ref_hash_ele_map.iteritems():
            print key
            print self.ref_hash_id_map[key]
            print value
            print "========================================================"

    def save_comp_tree(self):
        # print self.comp_tree.prettify()
        file = open("diffprint.html", "w+")
        str = self.comp_tree.prettify().encode('utf-8')
        # print str
        file.write(str)
        file.close()
