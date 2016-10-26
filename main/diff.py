import pagetree2
from bs4 import BeautifulSoup, NavigableString, Tag, Comment
import codecs
import difflib

class PageTreeDiff(object):
    ''''''
    ref_tree = ''
    comp_tree = ''
    ref_count = 0
    comp_count = 0
    ref_map = {}    #dict of element id and element hash
    comp_map = {}   #dict of element id and element hash
    ref_id_ele_map = {}
    comp_id_ele_map = {}
    comp_max_level = 0
    ref_max_level = 0
    diff_hash_list = [] #list of diff hashes between ref_map and comp_map
    diff_id_list = []   #list of diff ids between ref_map and comp_map
    folder = ""
    final_diff = {}
    diff_id_ele_list = None   #return diff id in this list
    unique_parents = None
    matching_ele_map = {}

    def __init__(self,ref_tree,ref_max_level,comp_tree,comp_max_level,folder ):
        self.ref_tree = ref_tree
        self.ref_max_level = ref_max_level
        self.comp_tree = comp_tree
        self.comp_max_level = comp_max_level
        self.__build_ref_tree(ref_tree)
        self.__build_comp_tree(comp_tree)
        self.folder = folder
        self.unique_parents = set()
        self.diff_id_ele_list = set()

    def __build_ref_tree(self, tree):
        if not isinstance(tree, NavigableString) and not isinstance(tree, Comment):
            for child in tree.children:
                if len(child) > 0:
                    # print "----"
                    if not isinstance(child, NavigableString) and not isinstance(tree, Comment):
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
        if not isinstance(tree, NavigableString) and not isinstance(tree, Comment):
            for child in tree.children:
                if len(child) > 0:
                    if not isinstance(child, NavigableString) and not isinstance(tree, Comment):
                        self.comp_map[child['id_diff_z1z']] = child['hash']
                        self.comp_id_ele_map[child['id_diff_z1z']] = child
                        self.comp_count += 1
                    self.__build_comp_tree(child)

    def print_comp_map(self):
        print "comp hash list size : ", len(self.comp_map.items())
        print self.comp_map.items()

    def find_diff_old(self):
        #only consider leaf nodes
        for comp_key, value in self.comp_map.iteritems():
            if value not in self.ref_map.values():
                self.diff_hash_list.append(value)
                self.diff_id_list.append(comp_key)
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
            prev_id = 0
            for id in self.diff_id_list:
                print id," - ",len(self.comp_id_ele_map[id].contents)
                id_ele = id, self.comp_id_ele_map[id]
                if(len(self.comp_id_ele_map[id].contents) == 1 and id - prev_id == 1):
                    diff_id_ele_list.append(id_ele)
                prev_id = id
            return diff_id_ele_list
            #self.__find_tag(self.ref_tree, self.comp_tree)

    def find_diff(self):

        # self.__recursive_diff(self.ref_tree.html, self.comp_tree.html)
        self.__find_diff(self.ref_tree.html, self.comp_tree.html)
        ref_file = codecs.open("../files/"+self.folder+"ref_tree.html", "w+", "UTF-8")
        comp_file = codecs.open("../files/"+self.folder+"comp_tree.html", "w+", "UTF-8")
        ref_file.write(self.ref_tree.prettify())
        comp_file.write(self.comp_tree.prettify())
        ref_file.close()
        comp_file.close()
        return self.diff_id_ele_list

    def __mark_extra_child(self, ele):
        if not isinstance(ele, NavigableString) and not isinstance(ele, int):
            ele['isExtraChild'] = 1;
        else:
            print "+++++"
            print ele
            pass

    def __find_diff(self, ref, comp):
        ref_set = []
        comp_set = []

        ref["isDiff"] = 0
        comp["isDiff"] = 0
        ref_set.append(ref)
        comp_set.append(comp)
        # print ref_set
        # return
        self.__recursive_diff(ref_set, comp_set)

        self.__find_attr_diff()

        self.__find_mark_ancestor(ref,0)
        self.__find_mark_ancestor(comp,1)


    def __find_mark_ancestor(self, node, flag):

        if not isinstance(node, NavigableString) and not isinstance(node, Comment):

            if node['isDiff'] >= 1:
                self.__mark_ancestor(node,flag)
            else:
                for child in node.contents:
                    self.__find_mark_ancestor(child,flag)

    def __mark_ancestor(self, node, flag):
        if node.parent != None and node.parent.name !='html':
            if node.parent['isDiff'] == -1:
                if flag == 0:
                    comp_ele = self.matching_ele_map[node.parent['id_diff_z1z']]
                    self.diff_id_ele_list.add(('*',node.parent['id_diff_z1z'], comp_ele))
                    self.diff_id_ele_list.add(('~',node['id_diff_z1z']))
                # node['isDiff'] = 3
                return
            self.__mark_ancestor(node.parent,flag)

    def __find_attr_diff(self):
        for ele in self.unique_parents:
            self.__recursive_compare_attr(ele[0], ele[1])

    def __recursive_compare_attr(self, obj1, obj2):
        if obj1.parent == None or obj2.parent == None:
            return
        # print obj1
        tag1 = str(obj1.encode("UTF-8"))
        tag2 = str(obj2.encode("UTF-8"))

        if isinstance(obj1, NavigableString) or isinstance(obj1, Comment) or isinstance(obj2, NavigableString) or isinstance(obj2, Comment):
            return

        obj1['isDiff'] = -1
        obj2['isDiff'] = -1
        self.matching_ele_map[obj1['id_diff_z1z']] = obj2['id_diff_z1z']
        # tag1.replace(str(obj1['hash']),"")
        # for ele in obj1.contents:
        #     if not isinstance(ele,NavigableString):
        #         # tag1.replace(str(ele['hash']),"")
        #         tag1.replace(str(ele.encode("UTF-8")),"")
        #     else:
        #         tag1.replace(str(ele.encode("UTF-8")),"")
        # tag2.replace(str(obj2['hash']),"")
        # for ele in obj2.contents:
        #     if not isinstance(ele,NavigableString):
        #         # tag2.replace(str(ele['hash']),"")
        #         tag2.replace(str(ele.encode("UTF-8")),"")
        #     else:
        #         tag2.replace(str(ele.encode("UTF-8")),"")
        tag1 = tag1[:tag1.find('>')]
        tag2 = tag2[:tag2.find('>')]
        st = tag1.find(str(obj1['hash']))
        le = len(str(obj1['hash']))
        tag1 = tag1[:st] + tag1[st+le:]

        st = tag2.find(str(obj2['hash']))
        le = len(str(obj2['hash']))
        tag2 = tag2[:st] + tag2[st+le:]


        print str(obj1['hash'])
        print "??????1"
        print obj1['id_diff_z1z']
        print "??????2"
        print obj2['id_diff_z1z']
        print "??????3"
        print tag1
        print "??????4"
        print tag2


        if hash(tag1)!=hash(tag2):
            obj1['hasDiffAttr'] = 1
            obj2['hasDiffAttr'] = 1
            self.diff_id_ele_list.add(('#',obj1, obj2))


        self.__recursive_compare_attr(obj1.parent, obj2.parent)



    def __recursive_diff(self, ref, comp):
        # if not isinstance(ref, NavigableString) and not isinstance(comp, NavigableString):

        hash_list_ref = []
        hash_list_comp = []
        hash_ele_map_ref = {}
        hash_ele_map_comp = {}
        unmatched_ref = []
        unmatched_comp = []
        unmatched_all = []
        unmatched_ref_children = []
        unmatched_comp_children = []
        unmatched_ref_children_unmatched = []
        unmatched_comp_children_unmatched = []
        unmatched_ref_children_map = {}
        unmatched_comp_children_map = {}

        for ele in ref:
            hash_list_ref.append(ele['hash'])
            hash_ele_map_ref[ele['hash']] = ele

        for ele in comp:
            hash_list_comp.append(ele['hash'])
            hash_ele_map_comp[ele['hash']] = ele

        for ele in hash_list_ref:
            if ele not in hash_list_comp:
                unmatched_ref.append(ele)
                unmatched_all.append(ele)
            else:
                self.unique_parents.add((hash_ele_map_ref[ele].parent,hash_ele_map_comp[ele].parent))

        for ele in hash_list_comp:
            if ele not in hash_list_ref:
                unmatched_comp.append(ele)
                unmatched_all.append(ele)
            else:
                self.unique_parents.add((hash_ele_map_ref[ele].parent,hash_ele_map_comp[ele].parent))

        #get a list of children of unmatched ref node
        for ele in unmatched_ref:
            for child in hash_ele_map_ref[ele].contents:
                if isinstance(child,NavigableString) or isinstance(child,Comment):
                    unmatched_ref_children.append(child)
                else:
                    unmatched_ref_children.append(child['hash'])
                    unmatched_ref_children_map[child['hash']] = child

        #get a list of children of unmatched comp node
        for ele in unmatched_comp:
            for child in hash_ele_map_comp[ele].contents:
                if isinstance(child,NavigableString) or isinstance(child,Comment):
                    unmatched_comp_children.append(child)
                else:
                    unmatched_comp_children.append(child['hash'])
                    unmatched_comp_children_map[child['hash']] = child


        for ele in unmatched_ref_children:
            if ele not in unmatched_comp_children:
                if isinstance(ele, NavigableString) or isinstance(ele, Comment):
                    ele.parent['isDiff'] = 2
                elif len(unmatched_ref_children_map[ele].contents) == 0:
                    unmatched_ref_children_map[ele]['isDiff'] = 1
                    self.diff_id_ele_list.add(('~',unmatched_ref_children_map[ele]['id_diff_z1z']))
                else:
                    unmatched_ref_children_unmatched.append(unmatched_ref_children_map[ele])
            else:
                for ele2 in unmatched_comp_children:
                    if ele2 == ele:
                        if not isinstance(ele2, NavigableString) and not isinstance(ele2, Comment) and not isinstance(ele, NavigableString) and not isinstance(ele, Comment):
                            self.unique_parents.add((unmatched_ref_children_map[ele], unmatched_comp_children_map[ele2]))
                        else:
                            self.unique_parents.add((ele, ele2))

        for ele in unmatched_comp_children:
            if ele not in unmatched_ref_children:
                if isinstance(ele, NavigableString) or isinstance(ele, Comment):
                    ele.parent['isDiff'] = 2
                elif len(unmatched_comp_children_map[ele].contents) == 0:
                    unmatched_comp_children_map[ele]['isDiff'] = 1
                    self.diff_id_ele_list.add(('~',unmatched_comp_children_map[ele]['id_diff_z1z']))
                else:
                    unmatched_comp_children_unmatched.append(unmatched_comp_children_map[ele])
            else:
                for ele2 in unmatched_ref_children:
                    if ele2 == ele:
                        if not isinstance(ele2, NavigableString) and not isinstance(ele2, Comment) and not isinstance(ele, NavigableString) and not isinstance(ele, Comment):
                            self.unique_parents.add((unmatched_ref_children_map[ele2], unmatched_comp_children_map[ele]))
                        else:
                            self.unique_parents.add((ele2, ele))

        if len(unmatched_ref_children_unmatched)>0 and len(unmatched_comp_children_unmatched)>0:
            self.__recursive_diff(unmatched_ref_children_unmatched, unmatched_comp_children_unmatched)
        return


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


