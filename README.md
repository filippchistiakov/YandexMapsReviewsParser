# YandexMapsReviewsParser

Парсер отзывов с Яндекс Карт.

## Описание

Сейчас реализована выгрузка данных в JSON. Выгружаю без преобразования, оно будет на другом этапе. 

Вот описание его структуры:

- `"selenium_id"`: Уникальный идентификатор отзыва в системе Selenium.
- `"datetime"`: Массив со всеми найденными датами и временем отзыва. Для некоторых старых отзывов удалось получить только дату без времени.
  - `"datePublished"`: Для большинства отзывов тут ISO 8601 дата и время
- `"review_rating"`: Объект с рейтингом отзыва.
  - `"bestRating"`: Максимальный рейтинг.
  - `"worstRating"`: Минимальный рейтинг.
  - `"ratingValue"`: Рейтинг отзыва.
- `"author"`: Информация об авторе отзыва.
  - `"image"`: URL-адрес изображения автора.
  - `"name"`: Имя автора.
- `"author_url"`: URL-адрес профиля автора отзыва.
- `"review_text"`: Текст отзыва.
- `"like"`: Количество лайков для отзыва.
- `"dislike"`: Количество дизлайков для отзыва.
- `"is_a_response"`: Булевое значение, указывающее, есть ли ответ от организации на этот отзыв.
- `"response_datetime"`: Текст с датой ответа на отзыв. _Тут имено дата, причем приходит она str_
- `"response_text"`: Текст ответа на отзыв.

## Запуск

```
python run.py --org_id 1124715036
```
Вместо параметра `org_id` необходимо указать идентификатор организации.


| `url`                                                  | `org_id`   |
|--------------------------------------------------------|------------|
| https://yandex.ru/maps/org/yandeks/1124715036/reviews/ | 1124715036 |

