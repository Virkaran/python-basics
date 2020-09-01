import requests
import json
from bs4 import BeautifulSoup

# function to scrap the coursera course details
def coursera_scrapper(search):

    # url of the page
    base_url = 'https://www.coursera.org/'
    r = requests.get(base_url+"search?query="+search)
    soup = BeautifulSoup(r.content, features="html.parser")
    courses=[]
    cards = soup.find_all('div', {'class':'card-info'})
    course = {}
    for card in cards:

        # details fetched
        course['course-title'] = card.find('h2').text
        rating_span = card.find('span', {'class':'ratings-text'})
        course['avg_rating'] = rating_span.text
        rating_count_span = card.find('span', {'class': 'ratings-count'}).find('span')
        course['rating_count'] = rating_count_span.text
        difficulty_span = card.find('span', {'class': 'difficulty'})
        course['difficulty'] = difficulty_span.text
        students_enrolled = card.find('span', {'class': 'enrollment-number'})
        course['students-enrolled'] = students_enrolled.text
        courses.append(course)

    json_data = json.dumps(courses)
    return(json_data)


# enter the course name to be searched
search_course = input("enter course name : ")
print(coursera_scrapper(search_course))
