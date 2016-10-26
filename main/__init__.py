import sys
import os
import time
import codecs
import pagetree2
import diff
import grab
import difflib

def main():
    #get page from selenium grabber
    url1 = "http://www.timeanddate.com/" #works well
    url2 = "http://www.time.gov/"	#selenium can't load all dynamic content. why??
    url3 = "http://www.worldtimeserver.com/current_time_in_IN.aspx"	#adobe download warning
    url4 = "http://wwp.greenwichmeantime.com/info/current-time/" #works well
    url5 = "http://www3.cs.stonybrook.edu/~aniahmed/page5.html" #works well
    url6 = "https://www.instagram.com/explore/tags/travel/"

    curr_time = time.strftime("%m-%d-%Y-%H-%M-%S/")
    print curr_time
    os.makedirs("../files/"+curr_time)


    '''
    CHANGE ENTRY FOR URL 1 on line 28
    '''
    print "First visit to page..."
    page1 = grab.grab(url5)
    page1_content = page1.get_dynamic_content(curr_time + "visit1.html")
    #create page tree from above
    page1_tree = pagetree2.PageTree2(page1_content)
    page1_tree.build_tree()

    #get page from selenium grabber again after t time
    print "Sleep for 5 secs"
    time.sleep(5)

    '''
    CHANGE ENTRY FOR URL 1 on line 42
    '''
    print "Second visit to page..."
    page2 = grab.grab(url5)
    page2_content = page2.get_dynamic_content(curr_time + "visit2.html")
    #create page tree from above too
    page2_tree = pagetree2.PageTree2(page2_content)
    page2_tree.build_tree()

    #DIFF between two direct visits
    print "Diff Stage - "
    base_diff = diff.PageTreeDiff(page1_tree.soup, page1_tree.max_level, page2_tree.soup, page2_tree.max_level, curr_time)
    diff_id_list = base_diff.find_diff()
    base_diff_file = codecs.open("../files/"+curr_time+"base_diff.txt", "w+")#, "utf-8")
    if diff_id_list is not None:
        for diff_item in diff_id_list:
            if diff_item[0] == '*':
                item1 = '*'
                diff_str = item1 + str(diff_item[1])+','+ str(diff_item[2])#+'\n'+str(diff_item[3])
                base_diff_file.write(diff_str)
                base_diff_file.write(';\n')
                continue
            elif diff_item[0] == '#':
                item1 = '#'
                diff_str = item1 + str(diff_item[1])+',' + str(diff_item[2])
                base_diff_file.write(diff_str)
                base_diff_file.write(';\n')
                continue
            elif diff_item[0] == '~':
                item1 = '~'
                diff_str = item1 + str(diff_item[1])#+',' + str(diff_item[2])
                # diff_str = item1 + diff_item[1].encode("UTF-8")+'\n'+'~~~~~~~~~~~~ '+'\n' + diff_item[2].encode("UTF-8")+'\n'
                base_diff_file.write(diff_str)
                base_diff_file.write(';\n')
                continue
            elif diff_item[0] == '+':
                item1 = '+'
                diff_str = item1 + str(diff_item[1])
                # diff_str = item1 + diff_item[1].encode("UTF-8")+'\n'
                base_diff_file.write(diff_str)
                base_diff_file.write(';\n')
            elif diff_item[0] == '-':
                item1 = '-'
                diff_str = item1 + str(diff_item[1])
                # diff_str = item1 + diff_item[1].encode("UTF-8")+'\n'
                base_diff_file.write(diff_str)
                base_diff_file.write(';\n')
    base_diff_file.close()

    #for each proxy
    #   access page through proxy
    #   get diff from initial page
    #   store diff as proxy diff
    #   compare diff with original diff and store result

    return

if __name__ == '__main__':
    main()

