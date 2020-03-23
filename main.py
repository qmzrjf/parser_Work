from user_agent import generate_user_agent
from utils import random_sleep, save_info_txt, save_info_json, seve_info_to_db

import requests
from bs4 import BeautifulSoup



# global variables
HOST = 'https://www.work.ua'
ROOT_PATH = '/ru/jobs/'
START_PAGE = 0


def main():
    page = START_PAGE

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
        response = requests.get(HOST + ROOT_PATH, params=payload, headers=headers)
        response.raise_for_status()

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        class_ = 'card card-hover card-visited wordwrap job-link'
        cards = soup.find_all('div', class_=class_)
        if not cards:
            cards = soup.find_all('div', class_=class_ + ' js-hot-block')

        result = []
        result_json = []
        if not cards:
            break

        dict_js = {}
        number = 0
        for card in cards:
            number+=1
            #get vacancy card name and link
            tag_a = card.find('h2').find('a')
            title = tag_a.text
            title = ''.join(x for x in title if x != "'")
            href = tag_a['href']

            # get vacancy full info
            response_in_page = requests.get(HOST + href, headers=headers)
            response_in_page.raise_for_status()

            html_in_page = response_in_page.text
            soup_in_page = BeautifulSoup(html_in_page, 'html.parser')

            print(response_in_page.url)

            # salary info
            class_salary = "text-black"
            salary = soup_in_page.find('b', class_=class_salary)

            if not salary:
                salary_min = 0
                salary_max = 0

            else:
                result_salary = salary.text
                salary = ''.join(x for x in result_salary if x.isdigit() or x == "–")
                ind = salary.find('–')
                if ind != -1:
                    salary_min = int(salary[:ind])
                    salary_max = int(salary[ind + 1:])
                else:
                    salary_min = int(salary)
                    salary_max = int(salary)

            # employer info
            class_employer = "text-indent text-muted add-top-sm"
            employer = soup_in_page.find_all('p', class_=class_employer)
            for i in employer:
                tag_a1 = i.find('a')
                if tag_a1:
                    emp_info = tag_a1.text
                    emp_href = tag_a['href'] #link to the employer profile on work

            # field info
            class_sphere = "add-top-xs"
            sphere = soup_in_page.find_all('span', class_=class_sphere)
            str = ""
            for i in sphere:
                str += i.text

            str = ''.join(x for x in str if x.isalpha() or x == " " or x == "," or x == ";")
            str = str.strip()
            ind = str.find(';')
            res_spher = str[:ind]

            # location, scheldule and requirements info
            class_lcr = "text-indent add-top-sm"
            lcr_info = soup_in_page.find_all('p', class_=class_lcr)
            str = ""
            for i in lcr_info:
                str += i.text
            str = ''.join(x for x in str if x.isalnum() or x ==" " or x ==".")
            str = str.split(" ")
            res = []
            for i in str:
                if i == '' or i == r"\n\n":
                   continue
                else:
                   res.append(i)
            str = ' '.join(x for x in res)
            city = res[0]
            ind = str.find('Показать телефон')
            if ind != -1:
                str = str[:ind] + str[ind + 17:]

            ind = str.find('кмотцентра')
            if ind != -1:
                str = str[:ind - 3] + str[ind + 20:]
            other_info = str
            print(other_info)

            result.append([title, href, salary_min, salary_max, emp_info, res_spher, city, other_info])
            result_array = [title, href, salary_min, salary_max, emp_info, res_spher, city,  other_info]
            dict_js.update({
                f"Vacancy on page {page}, number {number}": {
                    "Title": title,
                    "Link": href,
                    "Salary Minimum": salary_min,
                    "Salary Maximum": salary_max,
                    "Employer": emp_info,
                    "Field": res_spher,
                    "City": city,
                    "Other": other_info
                }
            })

            seve_info_to_db(result_array)

        save_info_txt(result)
        save_info_json(dict_js, page)


if __name__ == "__main__":
    main()
