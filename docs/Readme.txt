DIFF TOOL
=========

This diff tool can be used to find differences between 2 partially similar html pages at html element granularity.
If corresponding elements in two similar html pages have difference in attributes or difference in contents then it
will be recognized. The differences are found at the deepest level, i.e., if two corresponding elements are different 
because of difference in one of their chlidren then only the different children will be identified. 


For e.g- 

Page 1
-------

<html>
	<head>
		<tag1>
		</tag1>
</head>
<body>
	<tag2>
		<tag4>
			abc
		<tag4>

		<tag5>
			abc
		<tag5>
		
		<tag6>
			abc
		<tag6>

		<tag7>
			abc
		<tag7>

	</tag2>
	
	<tag3>
	</tag3>
</body>
</html>


Page 2
-------

<html>
	<head>
		<tag1>
		</tag1>
</head>
<body>
	<tag2>
		<tag4>
			xyz
		<tag4>

		<tag5>
			abc
		<tag5>
		
		<tag6>
			abc
		<tag6>

		<tag7>
			abc
		<tag7>

	</tag2>
	
	<tag3>
	</tag3>
</body>
</html>

In the above basic test case, only tag4 will be pointed out. Although the difference is within all the following - head, body, 
tag2 and tag4, the diff tool will find the deepest level of difference and point it out.


PRE-REQ
-------
While development and testing the following tools were used- 
1. Python 2.7.10
2. BeautifulSoup 4 : This is used to create a tree structure from the html source.
3. Selenium webdriver - version 2.53.1 : This is used to capture dynamic content from the webpage.


FILES
-----
1. docs/ - Has documentation related to the diff tool.
2. main/ -  Has the core source code for the diff tool.
3. tests/ - Has test code for running and testing diff tool. Also has test case for diff with proxy visits.
4. files/ - Has the diff generated output files. Files are kept in folders named on time at which tool was used.
	Folder within each directory are created on the basis of URL parts.
	For e.g. https://www.stonybrook.edu/~aniahmed/page5.html will have generate the following directory structure -
		files/date_and_time_of_day/cs_stonybrook_edu/~aniahmed/page5
	
	4.1. visit1.html	-	This is html dump of the first simple visit(not via proxy) of the webpage. All dynamic content is also captured.
	4.2. visit2.html	-	This is html dump of the second simple visit(not via proxy) of the webpage. All dynamic content is also captured.
	4.3. revisit1.html	-	This is html dump of the first proxy visit of the webpage. All dynamic content is also captured.
	4.4. visit3.html	-	This is html dump of the second proxy visit of the webpage. All dynamic content is also captured.
	4.5. ref_tree.html	-	This is called the reference tree. This is created from visit1.html. This has visit1.html tree along with useful metadata.
	4.6. comp_tree.html	-	This is called the comparison tree. This is created from visit2.html. This has visit2.html tree along with useful metadata.
	4.7. ref2_tree.html	-	This is created from second visit to the page without going through proxy.
	4.8. proxy_tree.html-	This is created from visiting the tree via proxy.
	4.9. base_diff_json.json 	-	This is the diff between visit1.html and visit2.html. This will tell us the dynamic parts of the page.
	4.10. proxy_diff_json.json 	-	This is the diff between a revisit1.html and visit3.html. This will give us the diff between the simple visit and the proxy visit.
	4.11. final_diff_json.json 	-	This is created from proxy_diff_json.json and base_diff_json.json. The elements of dynamic content from base_diff_json.json are ignored in proxy_diff_json.json to create final_diff_json.json
	4.12. oup.html		-	This file was used to generate logs while debugging.


CLASSES
-------
1. Grab 
	The purpose of this class is to grab the required content from the internet. It grabs the complete webpage i.e., both static and dynamic content. Selenium webdriver is used to load the page in Mozilla Firefox. After opening the page in firefox the driver waits for 5 seconds and captures the loaded version of the page. Before returning it quits firefox.

	Grab Class has 2 methods-

	1. get_dynamic_content(path) - Captures the page content directly, without going through a proxy.
		Argumets- path: the url of the page to be captured.
		Returns - complete page content as a string.

	2. get_dynamic_content_via_proxy(path, proxy_ip, proxy_port): - Captures the page content via a proxy.
		Argumets- path: the url of the page to be captured.
					proxy_ip: the IP address of the proxy.
					proxy_port: the port of the proxy.
		Returns - complete page content as a string.


2. PageTree
	This class is used to add structure to the captured html string by grab. Beautiful soup library is used to achieve this.

	PageTree class has parses the html string with a lxml parser. If the system doesnt have lxml parser installed then one of the following can be used to install it - 
		$ apt-get install python-lxml
		$ easy_install lxml
		$ pip install lxml

	The constructor of this class does the complete job of calling the Beautiful soup library and adding structure. 
	Other methods of the class are are redundent and were used for testing and bug fixing.


3. Diff
	This class has the core logic of the diff tool. 

	The constructor of the class takes the following arguments -
		
		__init__( ref_tree, comp_tree, folder)
		ref_tree - is the html tree for page 1 of comparision (ref_tree or ref2_tree).
		comp_tree - is the html tree for page 2 of comparison (comp_tree or proxy_tree).
		folder - is the path of the folder where all the relavant files for the current diff are to be generated and stored.

	The following is the used to get the diff - 

		find_diff(flag) - 
		Argument- flag: While comparing the first visit and second visit(both done without proxy), flag should be passed as 0.
					While comparing the revisit and proxy visit(one done via proxy), flag should be passed as 1.
		Returns- returns a list of lists of form - 

			[diff_ele_list, diff_attr_list]
			
			diff_ele_list is a list of elements that are different beacuse of additional or modified html element.
			diff_attr_list is a list of elemetns that are differnt because of difference in html tag attributes only.

			diff_ele_list is again made up of two lists - 
				[diff_ele_list_ref, diff_ele_list_comp]
				diff_ele_list_ref and diff_ele_list_comp do not necessarily contain correspoinding elements at corresponding index because correspondence cannot be made if elements are missing. But in basic cases we can visually get an idea of the corresponding elements. 

				Both diff_ele_list_ref and diff_ele_list_comp list is a list of tuples - 

					element[0] :  is the reduced string version of the html tag
					element[1] :  is the location of the html tag in the tree represented by string of following format -
						1.2.3.1
						This means the html tag is first child of the third child of the second child of the first element of the page.
						First element of the page is usually the <html> tag and second tag under it is usually the <body> tag.
						So 1.2.3.1 can refer to the first child of the third element of the body tag.

		This list is used to create the diff json files.



DESIGN
------




ALGORITHM
---------














