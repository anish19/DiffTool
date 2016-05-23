import sys
import time
import codecs
import pagetree
import diff
import grab

def main():
    #get page from selenium grabber
    url1 = "http://www.timeanddate.com/"
    #url1 = "http://www3.cs.stonybrook.edu/~aniahmed/page5.html"
    page1 = grab.grab(url1)
    page1_content = page1.get_dynamic_content("visit1.html")
    #create page tree from above
    page1_tree = pagetree.PageTree(page1_content)
    page1_tree.build_tree()

    #get page from selenium grabber again after t time
    time.sleep(5)

    page2_content = page1.get_dynamic_content("visit2.html")
    #create page tree from above too
    page2_tree = pagetree.PageTree(page2_content)
    page2_tree.build_tree()

    #DIFF between two direct visits
    base_diff = diff.PageTreeDiff(page1_tree.soup, page1_tree.max_level, page2_tree.soup, page2_tree.max_level)
    diff_id_list = base_diff.find_diff()
    base_diff_file = codecs.open("../files/base_diff.txt", "w+", "utf-8")
    if diff_id_list is not None:
        for diff_item in diff_id_list:
            base_diff_file.write(str(diff_item))
            base_diff_file.write('\n')
    base_diff_file.close()

    #for each proxy
    #   access page through proxy
    #   get diff from initial page
    #   store diff as proxy diff
    #   compare diff with original diff and store result

    return

if __name__ == '__main__':
    main()

