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

    ###########################################################################
    #Change proxy, port and url in te next lines to try different combinations
    ###########################################################################

    proxy_ip = "84.53.238.158"
    proxy_port = 80
    site_list = ["http://www.timeanddate.com"]

    curr_time = time.strftime("%m-%d-%Y-%H-%M-%S/")
    os.makedirs("../files/" + curr_time)

    i = 1
    for site in site_list:
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
        # page3_content = page3.get_dynamic_content_via_proxy(folder+ "visit3.html", proxy_ip, proxy_port)
        # page2_content = page2.get_dynamic_content_via_proxy(folder + "visit2.html", proxy_ip, proxy_port)

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
        json.dump(diff_json, base_diff_json_file, indent=4)
        base_diff_json_file.close()

        #First visit to page again...
        page1 = grab.grab(site)
        page1_content = page1.get_dynamic_content(folder+ "revisit1.html")
        # create page tree from above
        page1_tree = pagetree.PageTree(page1_content)
        page1_tree.build_tree()

        #visit via proxy
        page3 = grab.grab(site)

        # page3_content = page3.get_dynamic_content(folder+ "visit3.html")
        page3_content = page3.get_dynamic_content_via_proxy(folder+ "visit3.html", proxy_ip, proxy_port)
        # create page tree from above
        page3_tree = pagetree.PageTree(page3_content)
        page3_tree.build_tree()
        #get diff between page 1 and proxy
        print("\tstarting diff with proxy page")
        proxy_diff = diff.PageTreeDiff(page1_tree.soup, page3_tree.soup, folder)
        proxy_diff_list = proxy_diff.find_diff(1)
        diff_ele_list = proxy_diff_list[0]
        diff_attr_list = proxy_diff_list[1]
        print("\tproxy diff done")

        #write proxy_diff_json
        proxy_diff_json_file = codecs.open("../files/" + folder + "proxy_diff_json.json", "w+")
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
        json.dump(diff_json, proxy_diff_json_file, indent=4)
        proxy_diff_json_file.close()



        #################################
        #ignore base_diff from proxy_diff
        #################################
        print "removing base diff form proxy diff"
        base_diff_json_file = "../files/" + folder + "base_diff_json.json"
        with open(base_diff_json_file) as f:
            base_diff = json.load(f)

        proxy_diff_json_file = "../files/" + folder + "proxy_diff_json.json"
        with open(proxy_diff_json_file) as f:
            proxy_diff = json.load(f)

        ########Ignore ele diff
        #extract base diff keys for diff_ele into dict
        base_diff_ele = base_diff["diff_ele"]
        base_diff_ele_ref = {}
        for item in base_diff_ele["ref"]:
            for key in item:
                base_diff_ele_ref[key] = item[key]

        base_diff_ele_comp = {}
        for item in base_diff_ele["comp"]:
            for key in item:
                base_diff_ele_comp[key] = item[key]

        #extract proxy diff keys for diff_ele into dict
        proxy_diff_ele = proxy_diff["diff_ele"]
        proxy_diff_ele_ref = {}
        for item in proxy_diff_ele["ref"]:
            for key in item:
                proxy_diff_ele_ref[key] = item[key]

        proxy_diff_ele_comp = {}
        for item in proxy_diff_ele["comp"]:
            for key in item:
                proxy_diff_ele_comp[key] = item[key]

        #remove the mask from proxy diff
        for key in base_diff_ele_ref:
            if key in proxy_diff_ele_ref:
                del proxy_diff_ele_ref[key]

        for key in base_diff_ele_comp:
            if key in proxy_diff_ele_comp:
                del proxy_diff_ele_comp[key]


        #create final proxy diff
        proxy_diff_ele["ref"] = []
        proxy_diff_ele["comp"] = []

        for key,value in proxy_diff_ele_ref.iteritems():
            item = {}
            item[key] = value
            proxy_diff_ele["ref"].append(item)

        for key,value in proxy_diff_ele_comp.iteritems():
            item = {}
            item[key] = value
            proxy_diff_ele["comp"].append(item)

        final_diff = {}
        final_diff["diff_ele"] = {}
        final_diff["diff_ele"]["ref"] = proxy_diff_ele["ref"]
        final_diff["diff_ele"]["comp"] = proxy_diff_ele["comp"]

        ########Ignore attr diff
        base_diff_attr = base_diff["diff_attr"]
        proxy_diff_attr = proxy_diff["diff_attr"]

        base_diff_attr_ref_list = []
        base_diff_attr_comp_list = []

        for item in base_diff_attr:
            for key in item["ref"]:
                base_diff_attr_ref_list.append(key)

        for item in base_diff_attr:
            for key in item["comp"]:
                base_diff_attr_comp_list.append(key)

        rm_item_list = []
        for item in proxy_diff_attr:
            for key in item["ref"]:
                if key in base_diff_attr_ref_list:
                    rm_item_list.append(item)

        for item in proxy_diff_attr:
            for key in item["comp"]:
                if key in base_diff_attr_comp_list:
                    rm_item_list.append(item)

        for item in rm_item_list:
            if item in proxy_diff_attr:
                proxy_diff_attr.remove(item)

        print "creating final diff"
        final_diff["diff_attr"] = proxy_diff_attr
        final_diff_json_file = codecs.open("../files/" + folder + "final_diff_json.json", "w+")
        json.dump(final_diff, final_diff_json_file, indent=4)
        final_diff_json_file.close()
        print "final diff done"


if __name__ == '__main__':
    main()


