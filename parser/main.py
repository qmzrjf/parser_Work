from user_agent import generate_user_agent

import requests
from bs4 import BeautifulSoup

from config import config
from db_connect import create_db
from parse_tools import (
    get_vacancy_card_name_and_link, get_card, get_sphere,
    get_salary, get_employer, get_education, get_experience,
    get_city_and_other, get_title
)
from utils import save_info_txt, write_json, save_info_to_db


def main():
    create_db()
    page = config.START_PAGE

    while True:
        page += 1

        payload = {
            'ss': 1,
            'page': page,
        }

        user_agent = generate_user_agent()
        headers = {
            'User-Agent': user_agent,
        }

        page_number = f'PAGE: {page}'
        print(page_number)

        response = requests.get(config.HOST + config.ROOT_PATH, params=payload, headers=headers)
        response.raise_for_status()

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        class_ = 'card card-hover card-visited wordwrap job-link'
        cards = soup.find_all('div', class_=class_)
        if not cards:
            cards = soup.find_all('div', class_=class_ + ' js-hot-block')

        result = []
        if not cards:
            break

        for card in cards:

            href, vacancy_id = get_vacancy_card_name_and_link(card)

            soup_in_page = get_card(href, headers)

            title = get_title(soup_in_page)
            salary_min, salary_max = get_salary(soup_in_page)
            city, other = get_city_and_other(soup_in_page)
            employer, employer_href = get_employer(soup_in_page)
            sphere = get_sphere(soup_in_page)
            education = get_education(other)
            experience = get_experience(other)

            result.append([str(vacancy_id), str(title), str(config.HOST + href),
                           str(salary_min), str(salary_max), str(employer),
                           str(config.HOST + employer_href), str(sphere), str(city),
                           str(education), str(experience), str(other)])

            dict_js = {
                "Id": vacancy_id,
                "Title": title,
                "Link": config.HOST + href,
                "Salary Minimum": salary_min,
                "Salary Maximum": salary_max,
                "Employer": employer,
                "Employer Link": config.HOST + employer_href,
                "Sphere": sphere,
                "City": city,
                "Education": education,
                "Experience": experience,
                "Other": other
            }

            write_json(dict_js)
        save_info_txt(result)
        save_info_to_db(result)


if __name__ == "__main__":
    main()
