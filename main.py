import time
from selenium.webdriver import ActionChains

from functions import get_category_path, get_html_of_job, send_mail
from bs4 import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import os


class JobOffer(object):
    def __init__(self, details, requirements, link):
        self.details = details
        self.requirements = requirements
        self.link = link
    def get_job(self):
        return {
            'details': self.details,
            'requirements': self.requirements,
            'link': self.link
        }



def user_keyword():
    print("""
           ------------------------------------------------------------------------------------

                                            Job Web Scrapper
           ------------------------------------------------------------------------------------
    """)
    user_input = input("[+] Enter job you want to search > ")

    return user_input


def get_valid_job_requirments():
    with open('valid_requirements.txt', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip('\n')
            valid_job_requirements.add(line)
        f.close()


def show_full_details_of_jobs():
    last_height = driver.execute_script("return document.body.scrollHeight")
    try:
        while True:
            show_more_buttons = driver.find_elements_by_css_selector('.flex.primary--text.display-18.pointer.pc-view')
            for button in show_more_buttons:
                if button.is_displayed():
                    button.click()
            loading_button = driver.find_element_by_css_selector(".v-btn.v-btn--contained.theme--light.v-size--default.load_jobs_btn")
            actions = ActionChains(driver)
            actions.move_to_element(loading_button).perform()
            if loading_button:
                loading_button.click()
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
    except NoSuchElementException:
        pass
    except ElementClickInterceptedException:
        pass


def get_relevant_jobs():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    full_divs = soup.find_all('div', attrs={'class': 'flex job job-item'})
    div_list = soup.find_all('div', attrs={'class': 'flex job job-item preferred'})
    div_list.extend(full_divs)
    # Drushim site filter the jobs to preferred and regular jobs
    for full_div in div_list:
        div_text = full_div.text
        job_details_text = div_text[div_text.find('תיאור משרה'):div_text.rfind('דרישות התפקיד')]
        job_requirements_text = div_text[div_text.find('דרישות התפקיד'):div_text.rfind('<')]
        link = full_div.find('a', attrs={'title':'פתח משרה בחלון חדש'})['href']
        try:
            for word in valid_job_requirements:
                if word in job_requirements_text:
                    job = JobOffer(job_details_text, job_requirements_text, link)
                    job_object = job.get_job()
                    if job_object not in relevant_jobs:
                        relevant_jobs.append(job_object)
        except Exception as e:
            print("Error", e)

# extract job information and create body for our mail
def get_mail_content():
    content = ""
    for job in relevant_jobs:
        print(job)
        html = get_html_of_job(job, base_url)
        content += html
    return content




if __name__ == "__main__":
    keyword = user_keyword()
    base_url = 'https://www.drushim.co.il'
    relevant_jobs = []
    valid_job_requirements = set({})
    get_valid_job_requirments()
    url = get_category_path(keyword, base_url)

    # init driver
    os.environ["LANG"] = "en_US.UTF-8"
    driver = webdriver.Chrome(executable_path='C:\Program Files\JetBrains\chromedriver.exe')
    driver.maximize_window()
    driver.get(url)

    # click show more button to get full div details
    show_full_details_of_jobs()
    time.sleep(3)
    get_relevant_jobs()
    email_body = get_mail_content()
    receiver_email = 'practice.python123@gmail.com' # Password in READ.ME File
    send_mail(email_body, receiver_email)
    driver.close()
    driver.quit()



