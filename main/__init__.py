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

    print "First visit to page..."
    page1 = grab.grab(url6)
    page1_content = page1.get_dynamic_content(curr_time + "visit1.html")
    #create page tree from above
    page1_tree = pagetree2.PageTree2(page1_content)
    page1_tree.build_tree()

    #get page from selenium grabber again after t time
    print "Sleep for 5 secs"
    time.sleep(5)

    print "Second visit to page..."
    page2 = grab.grab(url6)
    page2_content = page2.get_dynamic_content(curr_time + "visit2.html")
    #create page tree from above too
    page2_tree = pagetree2.PageTree2(page2_content)
    page2_tree.build_tree()

    # page1_content=page1_content.encode('utf8')
    # page2_content=page2_content.encode('utf8')

    # fromlines = page1_content
    # tolines = page2_content
    #
    # diff = difflib.HtmlDiff().make_file(fromlines,tolines)
    #
    # print diff
    # base_diff_file = codecs.open("../files/"+curr_time+"python_diff.html", "w+")
    # base_diff_file.write(diff)

    # sys.stdout.writelines(diff)

    #DIFF between two direct visits
    print "Diff Stage - "
    base_diff = diff.PageTreeDiff(page1_tree.soup, page1_tree.max_level, page2_tree.soup, page2_tree.max_level, curr_time)
    diff_id_list = base_diff.find_diff()
    base_diff_file = codecs.open("../files/"+curr_time+"base_diff.txt", "w+")#, "utf-8")
    if diff_id_list is not None:
        for diff_item in diff_id_list:
            if diff_item[0] == '*':
                # with open("../files/"+curr_time+"/ref_tree.html","r") as refFile:
                #     for num1, line in enumerate(refFile, 1):
                #         if str(diff_item[1]) in line:
                #             break
                #
                # with open("../files/"+curr_time+"/comp_tree.html","r") as compFile:
                #     for num2, line in enumerate(compFile, 1):
                #         if str(diff_item[2]) in line:
                #             break
                item1 = '*'
                diff_str = item1 + str(diff_item[1])+','+ str(diff_item[2])
                # diff_str = item1 + str(diff_item[1])+'\n' +'**********' +'\n' + str(diff_item[2])+'\n'
                # diff_str = item1 + diff_item[1].encode("UTF-8")+'\n' +'**********' +'\n' + diff_item[2].encode("UTF-8")+'\n'
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
            # base_diff_file.write('id:')
            # base_diff_file.write(str(diff_item[0]))
            # base_diff_file.write('\nelement:')
            # base_diff_file.write(diff_item[1].encode("UTF-8"))
    base_diff_file.close()

    #for each proxy
    #   access page through proxy
    #   get diff from initial page
    #   store diff as proxy diff
    #   compare diff with original diff and store result

    return

if __name__ == '__main__':
    main()

