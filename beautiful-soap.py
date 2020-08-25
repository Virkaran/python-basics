# importing the beautifulsoap library
from bs4 import BeautifulSoup
html_doc = """
<html>
<head>
<meta http-equiv="Content-Type" content="text/html;
charset=iso-8859-1">
<title>An example of HTML page</title>
</head>
<body>
<h2>This is an example HTML page</h2>
<p>
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc at nisi velit,
aliquet iaculis est. Curabitur porttitor nisi vel lacus euismod egestas. In hac
habitasse platea dictumst. In sagittis magna eu odio interdum mollis. Phasellus
euismod porta.</p>
<p class id ="text1">this is a class text </p>
<p><a href="https://www.w3resource.com/html/HTML-tutorials.php"><i>Learn HTML 
from w3resource.com</i></a></p>
<p><a href="https://www.w3resource.com/css/CSS-tutorials.php"><i>Learn CSS from 
w3resource.com</i></a></p>
</body>
</html>
"""
# adding the html content in the beautifulsoap
# with the help of a HTML parser
soup = BeautifulSoup(html_doc, 'html.parser')

# gives the title tag content
print(soup.find("title"))

# print the content in the h2 heading tag 
print(soup.find("h2"))

# print the data in the anchor tag
print(soup.find("a"))


tag = soup.a
tag = tag.clear()

# print the data in the <a> tag only
print(soup.a)

tag1 = soup.p
print(type(tag1))


# print all the tags in the HTML page
for tag in soup.find_all(True):
    print(tag.name)



output :-
<title>An example of HTML page</title>
<h2>This is an example HTML page</h2>
<a href="https://www.w3resource.com/html/HTML-tutorials.php"><i>Learn HTML 
from w3resource.com</i></a>
<a href="https://www.w3resource.com/html/HTML-tutorials.php"></a>
<class 'bs4.element.Tag'>
html
head
meta
title
body
h2
p
p
p
a
p
a
i
