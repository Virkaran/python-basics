import pytest
from pennsylvania_scrapper import PennsylvaniaScrapper


def test_valid():
    # a valid data
    fname, lname, dob = 'William', 'Rios', '07/31/1975'
    expected_output = [{
        'docket_number': 'MJ-31201-CR-0001050-2007',
        'court_office': 'MDJ-31-2-01',
        'short_caption': 'Comm. v. Rios Rivera, William Antonio',
        'filling_date': '11/06/2007',
        'country': 'Lehigh',
        'case_status': 'Closed',
        'primary_participant': 'Rios Rivera, William Antonio',
        'OTN': 'K6846641',
        'complaint_number': '0790050',
        'police_incident': '0790050',
        'date_of_birth': '7/31/1975'
    }]

    scrapper = PennsylvaniaScrapper(
        'https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx', fname, lname, dob)
    actual_output = scrapper.scrap()

    assert expected_output == actual_output


def test_invalid():
    # a inn valid data
    fname, lname, dob = 'fname', 'lname', '12/11/2001'
    expected_output = {
        'docket_number': '',
        'court_office': '',
        'short_caption': '',
        'filling_date': '',
        'county': '',
        'primary_participant': '',
        'otn': '',
        'complaint_number': '',
        'dob': ''
    }

    scrapper = PennsylvaniaScrapper(
        'https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx', fname, lname, dob)
    actual_output = scrapper.scrap()

    assert expected_output == actual_output
