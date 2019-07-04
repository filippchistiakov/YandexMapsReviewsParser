from selenium.common.exceptions import (
    NoSuchElementException,
)
from datetime import datetime


# Это класс, с отзывом.
class Review(object):
    "class for reviews"

    # Вывод словаря атрибутов
    def __repr__(self):
        return repr(self.__dict__)

    # Расчет рейтинга
    def star_count(self, element):
        default_count = 0
        for star in element.find_elements_by_xpath(
            './/*[@class="business-rating-badge-view__stars"]/.//span'
        ):
            if "empty" not in star.get_attribute("class"):
                default_count += 1
        return default_count

    # Проверка наличия ответа на отзыв.
    def check_business_response(self, element):
        try:
            business_review = element.find_element_by_xpath(
                './/*[@class="business-review-view__comment"]'
            )
            business_review.click()
            return BusinessResponse(business_review)
        except NoSuchElementException:
            return BusinessResponse(None)

    # Основная ф-ция инициализации, которая принимает <selenium.webdriver.firefox.webelement.FirefoxWebElement> на вход с отзывом
    def __init__(self, element):
        try:
            # ID автора
            self.author_id = (
                element.find_element_by_css_selector(
                    "a.user-icon-view"
                )
                .get_attribute("href")
                .replace("https://yandex.ru/ugcpub/pk/", "")
                .replace("http://yandex.ru/ugcpub/pk/", "")
            )
            # self.author_id = (
            #     element.find_element_by_xpath('.//*[@class="user-icon-view"]')
            #         .get_attribute("href")
            #         .replace("https://yandex.ru/ugcpub/pk/", "")
            #         .replace("http://yandex.ru/ugcpub/pk/", "")
            # )
        except NoSuchElementException:
            pass
        try:
            # Имя пользователя
            self.author_name = element.find_element_by_xpath(
                './/*[@class="business-review-view__author"]/.//span'
            ).text
        except NoSuchElementException:
            pass
        try:
            # Уровень пользователя
            self.author_profession = int(
                "".join(
                    filter(
                        str.isdigit,
                        element.find_element_by_xpath(
                            './/*[@class="business-review-view__author-profession"]'
                        ).text,
                    )
                )
            )
        except NoSuchElementException:
            pass
        try:
            # Оценка пользователя
            self.stars = self.star_count(element)
        except NoSuchElementException:
            pass
        try:
            # Дата и время отправки отзыва !!!ПРОВЕРИТЬ ТАЙМЗОНУ!!!
            self.datetime = datetime.strptime(
                element.find_element_by_xpath(
                    './/*[@class="business-review-view__date"]//meta[@itemprop="datePublished"]'
                ).get_attribute("content"),
                "%Y-%m-%dT%H:%M:%S.%fZ",
            )
        except NoSuchElementException:
            pass
        try:
            self.text = element.find_element_by_xpath(
                './/*[@class="business-review-view__body"]'
            ).text.replace("\n", "")
        except NoSuchElementException:
            pass
        try:
            self.like = int(
                element.find_element_by_xpath(
                    './/*[@class="business-reactions-view__icon"]/following-sibling::*'
                ).text
            )
        except NoSuchElementException:
            self.like = 0
        try:
            self.dislike = int(
                element.find_element_by_xpath(
                    './/*[@class="business-reactions-view__icon _dislike"]/following-sibling::*'
                ).text
            )
        except NoSuchElementException:
            self.dislike = 0
        try:
            business_review = element.find_element_by_xpath(
                './/*[@class="business-review-view__comment"]'
            )
            business_review.click()

            self.response_flag = True
            # Название организации
            self.response_title = element.find_element_by_xpath(
                './/*[@class="business-review-view__comment-title"]'
            ).text
            # Дата и время отправки отзыва !!!ПРОВЕРИТЬ ТАЙМЗОНУ!!!
            self.response_datetime = element.find_element_by_xpath(
                './/*[@class="business-review-view__date _org-answer"]'
            ).text
            self.response_text = element.find_element_by_xpath(
                './/*[@class="business-review-view__body _org-answer"]'
            ).text.replace(
                "\n", ""
            )
        except NoSuchElementException:
            pass
