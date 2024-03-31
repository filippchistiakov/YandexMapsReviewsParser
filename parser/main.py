import time
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from parser.classes import Review
import datetime as dt
import os
from tqdm import tqdm
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

# log lower levels to stdout
stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.addFilter(lambda rec: rec.levelno <= logging.INFO)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

# log higher levels to stderr (red)
stderr_handler = logging.StreamHandler(stream=sys.stderr)
stderr_handler.addFilter(lambda rec: rec.levelno > logging.INFO)
stdout_handler.setFormatter(formatter)
logger.addHandler(stderr_handler)


def save_json(data, file_type, path, id, file_dttm):
    json_file_name = os.path.join(path, f'{id}_{file_type}_{file_dttm}.json')
    with open(json_file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
    logger.info(f'Saved {json_file_name}')


def get_organization_reviews(org_id: int = 1124715036, **kwargs):
    organization_url = f"https://yandex.ru/maps/org/yandeks/{org_id}/reviews/"
    logger.info(f'Start {organization_url=}')
    path = os.path.join(os.getcwd(), 'json')
    file_dttm = dt.datetime.now(dt.UTC)

    with webdriver.Firefox() as driver:
        driver.get(organization_url)
        total_reviews_text = driver.find_element(by=By.XPATH,
                                                 value='//*[@class="card-section-header__title _wide"]').text
        total_reviews_int = int(re.sub(r'\D', '', total_reviews_text))
        reviews_selenium_elems = set()
        pbar = tqdm(total=total_reviews_int)
        pbar.set_description("Loading all reviews on the page")
        while total_reviews_int != len(reviews_selenium_elems):
            tqdm_saved_len = len(reviews_selenium_elems)
            for review_elem in driver.find_elements(by=By.XPATH, value='//*[@class="business-review-view__info"]'):
                reviews_selenium_elems.add(review_elem)
                driver.execute_script("arguments[0].scrollIntoView(true);", review_elem)
            pbar.update(len(reviews_selenium_elems) - tqdm_saved_len)
            time.sleep(0.3)
        pbar.close()
        logger.info(f"FINISH {len(reviews_selenium_elems)=}")

        data = []
        for review_elem in tqdm(reviews_selenium_elems):
            new_review = Review()
            new_review.parse_base_information(review_elem=review_elem)
            new_review.try_add_responce(review_elem=review_elem, driver=driver)
            data.append(new_review.__dict__)

        save_json(data, 'reviews', path, org_id, file_dttm)

        def experimental():
            script_element = driver.find_element(by=By.XPATH, value='//script[@class="state-view"]')
            script_content = script_element.get_attribute("innerHTML")
            data = json.loads(script_content)
            save_json(data, 'script_content', path, org_id, file_dttm)

        experimental()


if __name__ == '__main__':
    pass
