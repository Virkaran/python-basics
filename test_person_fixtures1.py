import pytest
from Person import Person

#adding the name 
@pytest.fixture
def person_name():
    return 'joe'

#adding the year 
@pytest.fixture
def year():
    return 1899

#function for deploying the values 
def test_person_name(person_name,year):
    person= Person(person_name,year)

    assert person.name == person_name
