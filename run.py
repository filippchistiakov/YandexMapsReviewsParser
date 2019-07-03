from selenium import webdriver
from classes import Review

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException


print("Стандартная: https://yandex.ru/maps/org/yandeks/1124715036/")
print("default для запуска стандартной")
url = input("Ввести ссылку на отзывы :")
if url == "default":
    url = 'https://yandex.ru/maps/org/yandeks/1124715036/'
driver = webdriver.Firefox()
driver.get(
    url
)
print("Начал нажимать на кнопку посмотреть еще отзывы.")
while True:
    try:
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
        print('"еще" не найденно. Страницу прокрутили до конца' )
        break
while (
    len(driver.find_elements_by_xpath('//*[@class="business-review-view__expand"]')) > 5
):
    print(
        len(driver.find_elements_by_xpath('//*[@class="business-review-view__expand"]'))
    )
    more_buttons = driver.find_elements_by_xpath(
        '//*[@class="business-review-view__expand"]'
    )
    for more_button in more_buttons:
        try:
            more_button.click()
        except ElementNotInteractableException:
            pass
    break

reviews = driver.find_elements_by_xpath('//*[@class="business-review-view _wide"]')
reviews_list = []
for rev in reviews:
    driver.execute_script("arguments[0].scrollIntoView(true);", rev)
    try:
        reviews_list.append(Review(rev).__dict__)
    except:
        pass

# Мы получает list
with open('response.txt', 'w') as f:
    for item in reviews_list:
        f.write("%s\n" % item)