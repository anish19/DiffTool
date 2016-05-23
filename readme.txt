README
------

Requires 
	- Python 2.7.10
	- urllib2
	- selenium 2.53.1
	- BeautifulSoup 4


1. __init__.py starts the program.

2. files/ folder has one sample output set.
	- The sample output is for webpage http://www.timeanddate.com/
	- visit1.html stores the exact html rendered after 5 secs the page is rendered by firefox.
	- sleep for 5 secs
	- visit2.html stores the exact html rendered after 2nd visit of page.
	- ref_tree.html is constructed using visit1.html. This has additional meta data added by us on reference page.
	- comp_tree.html is constructed using visit2.html. This has additioanl meta data added by us on compared page.
	- the additional meta data is level, id, hash, etc...
	- base_diff.txt has list of element identifiers that are different between the two visits.
	

	Eg.

	visit1.html
	----------
		<html>
			<head>
				Hi
			</head>
			<body>
				23
			</body>
		</html>

	
	visit2.html
	----------
		<html>
			<head>
				Hi
			</head>
			<body>
				24
			</body>
		</html>


	ref_tree.html
	-------------
		<html level='0' id='0' hash='123'>
			<head level='1' id='1' hash='456'>
				Hi
			</head>
			<body level='1' id='2' hash='789'>
				23
			</body>
		</html>


	comp_tree.html
	-------------
		<html level='0' id='0' hash='111'>
			<head level='1' id='1' hash='456'>
				Hi
			</head>
			<body level='1' id='2' hash='777'>
				234
			</body>
		</html>

	base_diff.txt
	-------------
		0
		2

	
	Explaination-
	In base_diff.txt, 0 refers to the html element and 2 refers to the body element. So base_diff.txt has a \n seperated list of identifers that lead us to the different elements.



	- The sample provided in files/ is for timeanddate.com. 0, 21, 22....310 are identifiers of elements of the tree. The element 310 can be seen on line 736 of both files. This line has value of seconds shown in the website. They differ by 10 secs and have been identifed. 0,21,22...309 are parents of 310.
