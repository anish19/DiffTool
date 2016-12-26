import sys
import os
import time
import codecs
import json

def main():
    sys.path.insert(0, '../main')
    import pagetree
    import diff
    import grab

    print "Start"
    site_test = [ "http://www3.cs.stonybrook.edu/~aniahmed/page5.html"]

    site_list1 = [   'https://www.google.com/',
                    # 'https://www.youtube.com/',
                    'https://www.facebook.com/',
                    'https://www.baidu.com/',
                    'https://www.yahoo.com/',
                    # 'https://www.amazon.com/',
                    'https://www.wikipedia.com/',
                    'https://www.qq.com/',
                    'http://www.google.co.in',
                 ]

    site_list2 = [
                    'https://www.twitter.com/',
                    'https://www.live.com/',
                    #'https://www.taobao.com/',
                    'http://www.google.co.jp',
                    "http://www.bing.com",
                    "http://www.instagram.com",
                    "http://www.weibo.com",
                    "http://www.sina.com.cn",
                    "http://www.linkedin.com",
                    "http://www.yahoo.co.jp",
                ]

    site_list3 = [
                    "http://www.msn.com",
                    "http://www.vk.com",
                    "http://www.google.de",
                    "http://www.yandex.ru",
                    "http://www.hao123.com",
                    "http://www.google.co.uk",
                    "http://www.reddit.com",
                    "http://www.ebay.com",
                    "http://www.google.fr",
                    "http://www.t.co",
                    "http://www.tmall.com",
                ]

    site_list4 = [
                    "http://www.google.com.br",
                    "http://www.360.cn",
                    "http://www.sohu.com",
                    "http://www.amazon.co.jp",
                    "http://www.pinterest.com",
                    "http://www.mail.ru",
                    "http://www.onclickads.net",
                    "http://www.netflix.com",
                    "http://www.google.it",
                    "http://www.google.ru",
                  ]

    site_list5 = [
                    "http://www.microsoft.com",
                    "http://www.google.es",
                    "http://www.wordpress.com",
                    "http://www.gmw.cn",
                    "http://www.tumblr.com",
                    "http://www.paypal.com",
                    "http://www.blogspot.com",
                    "http://www.imgur.com",
                    "http://www.stackoverflow.com",
                    "http://www.aliexpress.com",
                ]

    site_list6 = [
                    "http://www.Naver.com",
                    "http://www.ok.ru",
                    "http://www.apple.com",
                    "http://www.github.com",
                    "http://www.google.com.mx",
                    "http://www.chinadaily.com.cn",
                    "http://www.xvideos.com",
                    "http://www.imdb.com",
                    "http://www.google.co.kr",
                    "http://www.pornhub.com",
                  ]

    site_list7 = [
                    "http://www.fc2.com",
                    "http://www.jd.com",
                    "http://www.blogger.com",
                    #"http://www.163.com",
                    "http://www.google.ca",
                    "http://www.google.com.hk",
                    "http://www.xhamster.com",
                    "http://www.whatsapp.com",
                    "http://www.amazon.in",
                    "http://www.office.com",
                ]

    site_list8 = [
                    "http://www.google.com.tr",
                    "http://www.tianya.cn",
                    "http://www.google.co.id",
                    "http://www.youku.com",
                    "http://www.rakuten.com.jp",
                    "http://www.craigslist.org",
                    "http://www.amazon.de",
                    "http://www.bongacams.com",
                    "http://www.nicovideo.jp",
                    "http://www.google.pl",
                ]

    site_list9 = [
                    "http://www.soso.com",
                    "http://www.bilibili.com",
                    "http://www.dropbox.com",
                    "http://www.xinhuanet.com",
                    "http://www.outbrain.com",
                    "http://www.pixnet.com",
                    "http://www.alibaba.com",
                    "http://www.alipay.com",
                    "http://www.microsoftonline.com",
                    "http://www.google.com.tw",
                ]

    site_list10 = [
                    "http://www.booking.com",
                    "http://www.googleusercontent.com",
                    "http://www.google.com.au",
                    "http://www.popads.net",
                    "http://www.cntv.cn",
                    "http://www.zhihu.com",
                    "http://www.amazon.co.uk",
                    "http://www.diply.com",
                    "http://www.coccoc.com",
                    "http://www.cnn.com"
                ]

    curr_time = time.strftime("%m-%d-%Y-%H-%M-%S/")
    os.makedirs("../files/" + curr_time)
    i = 1

    ######################################################
    #change in next line to try different set of website
    ######################################################
    for site in site_test:
        print i," ",site ," :"
        i +=1
        name = site.split('.')
        if len(name) == 3:
            name = name[1]+"_"+name[2]
        elif len(name) >= 4:
            name = name[1]+"_"+name[2]+"_"+name[3]
        folder = curr_time+name
        os.makedirs("../files/" + folder)
        folder = curr_time + name + "/"

        #First visit to page...
        page1 = grab.grab(site)
        page1_content = page1.get_dynamic_content(folder+ "visit1.html")
        # create page tree from above
        page1_tree = pagetree.PageTree(page1_content)
        page1_tree.build_tree()

        # get page from selenium grabber again after 5 time
        time.sleep(5)

        #Second visit to page...
        page2 = grab.grab(site)
        page2_content = page2.get_dynamic_content(folder + "visit2.html")
        # create page tree from above too
        page2_tree = pagetree.PageTree(page2_content)
        page2_tree.build_tree()

        print("\tstarting diff")
        base_diff = diff.PageTreeDiff(page1_tree.soup, page2_tree.soup, folder)
        diff_list = base_diff.find_diff(0)
        diff_ele_list = diff_list[0]
        diff_attr_list = diff_list[1]
        print("\tdiff done")

        #write diff to json file
        base_diff_json_file = codecs.open("../files/" + folder + "base_diff_json.json", "w+")
        diff_json = {}

        if diff_ele_list is not None:
            diff_ele_list_ref = diff_ele_list[0]
            diff_ele_list_comp = diff_ele_list[1]

            all_R_diff_ele = []
            for item in diff_ele_list_ref:
                R_diff_ele = {}
                R_diff_ele[item[1]] = item[0]
                all_R_diff_ele.append(R_diff_ele)

            all_C_diff_ele = []
            for item in diff_ele_list_comp:
                C_diff_ele = {}
                C_diff_ele[item[1]] = item[0]
                all_C_diff_ele.append(C_diff_ele)

            diff_ele = {}
            diff_ele["R"] = all_R_diff_ele
            diff_ele["C"] = all_C_diff_ele

            diff_json["diff_ele"] = {}
            diff_json["diff_ele"]["ref"] = diff_ele["R"]
            diff_json["diff_ele"]["comp"] = diff_ele["C"]

        attr_list = []
        for item in diff_attr_list:
            attr_ele = {}

            attr_ref_entry = {}
            attr_ref_entry [item[0][1]] = item[0][0]
            attr_ele["ref"] = attr_ref_entry

            attr_comp_entry = {}
            attr_comp_entry [item[1][1]] = item[1][0]
            attr_ele["comp"] = attr_comp_entry

            attr_list.append(attr_ele)

        diff_json["diff_attr"] = attr_list
        #pp = pprint.PrettyPrinter(indent=4, stream=base_diff_json_file)
        #diff_json = str(diff_json)
        #diff_json = diff_json.replace("'", '"')
        # diff_json = ast.literal_eval(diff_json)
        #pp.pprint(diff_json)
        json.dump(diff_json, base_diff_json_file, indent=4)

        base_diff_json_file.close()


if __name__ == '__main__':
    main()


