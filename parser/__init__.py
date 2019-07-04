from selenium import webdriver


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from .database import Session, ReviewModel
from .classes import Review

from sqlalchemy.exc import IntegrityError
import time


def parser_reviews(url='https://yandex.ru/maps/org/yandeks/1124715036/', **kwargs):
    driver = webdriver.Firefox()
    driver.get(
        url
    )
    print("Начал нажимать на кнопку посмотреть еще отзывы.")
    while True:
        try:
            time.sleep(3) #Иначе он крутит страницу быстрее и появляються дубли отзывов
            view_more_button = driver.find_element_by_xpath(
                '//*[@class="orgpage-reviews-view__more"]'
            )
            WebDriverWait(driver, 10).until_not(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@class="orgpage-reviews-view__loader"]')
                )
            )
            view_more_button.click()
        except NoSuchElementException:
            print('Страницу прокрутили до конца.' )
            break
    more_buttons = driver.find_elements_by_xpath(
        '//*[@class="business-review-view__expand"]'
    )
    for more_button in more_buttons:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
            time.sleep(1)
            more_button.click()
        except ElementNotInteractableException:
            pass

    reviews = driver.find_elements_by_xpath('//*[@class="business-review-view__info"]')
    print("Отзывов найденно: {}".format(len(reviews)))
    for review in reviews:
        driver.execute_script("arguments[0].scrollIntoView(true);", review)
        session = Session()
        new_review = Review(review).__dict__
        new_review_model = ReviewModel(**new_review)
        session.add(new_review_model)
        try:
            session.commit()
        except IntegrityError as e:
            print(e)
        session.close()
    driver.close()