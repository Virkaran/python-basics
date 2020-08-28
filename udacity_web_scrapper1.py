import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.udacity.com/courses/all')
soup = BeautifulSoup(r.content, features="html.parser")


# fetching the title of the courses
course_list = []
list_of_cources = soup.find('ul', {'class': 'catalog-cards__list'})
cources = list_of_cources.find_All('li', {'class': 'catalog-cards__list__item'})
for course in cources:
    course_list.append(course)
    print(course)



