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

In the above case, only tag4 will be pointed out. Although the difference is within all the following - head, body, 
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
	
	4.1. visit1.html	-
	4.2. visit2.html	-
	4.3. revisit1.html	-
	4.4. visit3.html	-
	4.5. ref_tree.html	-
	4.6. comp_tree.html	-
	4.7. ref2_tree.html	-
	4.8. proxy_tree.html-
	4.9. base_diff_json.json 	-
	4.10. proxy_diff_json.json 	-
	4.11. final_diff_json.json 	-
	4.12. oup.html		-


CLASSES
-------
1. Grab 


2. PageTree


3. Diff



DESIGN
------




ALGORITHM
---------














