from user_agent import generate_user_agent
from utils import save_info_txt, write_json, save_info_to_db

import requests
from bs4 import BeautifulSoup



# global variables
HOST = 'https://www.work.ua'
ROOT_PATH = '/ru/jobs/'
START_PAGE = 0


def _get_vacancy_card_name_and_link(card):
    tag_a = card.find('h2').find('a')
    title = tag_a.text
    title = ''.join(x for x in title if x != "'")
    href = tag_a['href']
    id_vac = ''.join(x for x in href if x.isdigit())
    return href, title, tag_a, id_vac


def _get_card_info(href, headers):
    response_in_page = requests.get(HOST + href, headers=headers)
    response_in_page.raise_for_status()
    print(response_in_page.url)
    html_in_page = response_in_page.text
    soup_in_page = BeautifulSoup(html_in_page, 'html.parser')
    return soup_in_page


def _get_salary_info(soup_in_page):
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
           salary_max = int(salary[ind+1:])
        else:
            salary_min = int(salary)
            salary_max = int(salary)
    return salary_min, salary_max


def _get_employer_info(soup_in_page, tag_a):
    class_employer = "text-indent text-muted add-top-sm"
    employer = soup_in_page.find_all('p', class_=class_employer)
    for i in employer:
        tag_a1 = i.find('a')
        if tag_a1:
            emp_info = tag_a1.text
            emp_info = ''.join(x for x in emp_info if x != "'")
            emp_href = tag_a['href']  # link to the employer profile on work
            return emp_info


def _get_field_info(soup_in_page):
    class_sphere = "add-top-xs"
    sphere = soup_in_page.find_all('span', class_=class_sphere)
    ver_str = ""
    for i in sphere:
        ver_str += i.text
    ver_str = ''.join(x for x in ver_str if x.isalpha() or x == " " or x == "," or x == ";")
    ver_str = ver_str.strip()
    ind = ver_str.find(';')
    res_spher = ver_str[:ind]

    ind = res_spher.find('Показать телефон')
    if ind != -1:
        res_spher = res_spher[:ind] + res_spher[ind+17:]

    ind = res_spher.find('кмотцентра')
    if ind != -1:
        res_spher = res_spher[:ind-3] + res_spher[ind + 20:]

    ind = res_spher.find('На карт')
    if ind != -1:
        res_spher = res_spher[:ind - 3] + res_spher[ind + 7:]

    field_info = res_spher
    return field_info


def _get_city_and_other_info(soup_in_page):
    class_lcr = "text-indent add-top-sm"
    lcr_info = soup_in_page.find_all('p', class_=class_lcr)
    ver_str = ""
    for i in lcr_info:
        ver_str += i.text
    ver_str = ''.join(x for x in ver_str if x.isalnum() or x == " " or x == "." or x == ",")
    ver_str = ver_str.split(" ")
    res = []
    for i in ver_str:
        if i == '' or i == r"\n\n":
            continue
        else:
            res.append(i)
    ver_str = ' '.join(x for x in res)
    city = res[0]
    city = ''.join(x for x in city if x.isalpha())


    ind = ver_str.find('Показать телефон')
    if ind != -1:
        ver_str = ver_str[:ind] + ver_str[ind+17:]

    ind = ver_str.find('кмотцентра')
    if ind != -1:
        ver_str = ver_str[:ind-3] + ver_str[ind + 20:]
    other_info = ver_str

    return city, other_info


def _get_education_info(other_info):

    str_educ = 'Высшее образование'
    ind_educ = other_info.find(str_educ)
    str_educ_not = 'Неоконченное высшее образование'
    ind_educ_not = other_info.find(str_educ_not)

    if ind_educ != -1:
        educ = other_info[ind_educ:ind_educ+len(str_educ)]
    elif ind_educ_not != -1:
        educ = other_info[ind_educ_not:ind_educ_not+len(str_educ_not)]
    else:
        educ = 'Не указано'

    return educ


def _get_experience_info(other_info):
    str_exp_one = 'Опыт работы от 1 года'
    ind_exp_one = other_info.find(str_exp_one)
    str_exp_two = 'Опыт работы от 2 лет'
    ind_exp_two = other_info.find(str_exp_two)
    str_exp_five = 'Опыт работы от 5 лет'
    ind_exp_five = other_info.find(str_exp_five)

    if ind_exp_one != -1:
        exp = other_info[ind_exp_one:ind_exp_one+len(str_exp_one)]
    elif ind_exp_two != -1:
        exp = other_info[ind_exp_two:ind_exp_two+len(str_exp_two)]
    elif ind_exp_five != -1:
        exp = other_info[ind_exp_five:ind_exp_five+len(str_exp_five)]

    else:
        exp = 'Не указано'

    return exp


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
        if not cards:
            break

        for card in cards:

            href_title_tag_a_id = _get_vacancy_card_name_and_link(card)
            soup_in_page = _get_card_info(href_title_tag_a_id[0], headers)
            salary = _get_salary_info(soup_in_page)
            city_and_other = _get_city_and_other_info(soup_in_page)

            href = href_title_tag_a_id[0]
            title = href_title_tag_a_id[1]
            tag_a = href_title_tag_a_id[2]
            id_vac = href_title_tag_a_id[3]
            salary_min = salary[0]
            salary_max = salary[1]
            employer = _get_employer_info(soup_in_page, tag_a)
            field = _get_field_info(soup_in_page)
            city = city_and_other[0]
            other = city_and_other[1]
            education = _get_education_info(other)
            experience = _get_experience_info(other)

            result.append([str(id_vac), str(title), str(href), str(salary_min), str(salary_max), str(employer),
                           str(field), str(city), str(education), str(experience), str(other)])
            dict_js ={

                    "Id": id_vac,
                    "Title": title,
                    "Link": href,
                    "Salary Minimum": salary_min,
                    "Salary Maximum": salary_max,
                    "Employer": employer,
                    "Field": field,
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
