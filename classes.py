# Класс Автора
class Autor(object):
    def __init__(self, element):
        # Имя пользователя
        self.author_name = element.find_element_by_xpath(
            './/*[@class="business-review-view__author"]/.//span'
        ).text
        # Уровень пользователя
        self.author_profession = element.find_element_by_xpath(
            './/*[@class="business-review-view__author-profession"]'
        ).text


# Это класс, ответа на отзыв. Он не может быть самостоятельным. Он часть отзыва - Review
class BusinessResponse(object):
    "class for business response"
    # Вывод словаря атрибутов
    def __repr__(self):
        return repr(self.__dict__)

    # Основная ф-ция инициализации, которая принимает <selenium.webdriver.firefox.webelement.FirefoxWebElement> на вход с отзывом
    def __init__(self, element):
        if element is None:
            self.response = False
            self.text = None
        else:
            self.response = True
            # Название организации
            self.title = element.find_element_by_xpath(
                './/*[@class="business-review-view__comment-title"]'
            ).text
            # Дата и время отправки отзыва !!!ПРОВЕРИТЬ ТАЙМЗОНУ!!!
            self.datetime = element.find_element_by_xpath(
                './/*[@class="business-review-view__date _org-answer"]'
            ).text
            self.text = element.find_element_by_xpath(
                './/*[@class="business-review-view__body _org-answer"]'
            ).text.replace("\n","")


# Это класс, с отзывом. Иногда у него может быть ответ на отзыв BusinessResponse а иногда нет.
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
        # Имя пользователя
        self.author_name = element.find_element_by_xpath(
            './/*[@class="business-review-view__author"]/.//span'
        ).text
        # Уровень пользователя
        self.author_profession = element.find_element_by_xpath(
            './/*[@class="business-review-view__author-profession"]'
        ).text
        # Оценка пользователя
        self.stars = self.star_count(element)
        # Дата и время отправки отзыва !!!ПРОВЕРИТЬ ТАЙМЗОНУ!!!
        self.datetime = datetime.strptime(
            element.find_element_by_xpath(
                './/*[@class="business-review-view__date"]//meta[@itemprop="datePublished"]'
            ).get_attribute("content"),
            "%Y-%m-%dT%H:%M:%S.%fZ",
        )
        self.text = element.find_element_by_xpath(
            './/*[@class="business-review-view__body"]'
        ).text.replace("\n","")
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

        self.businessresponse = self.check_business_response(element)