**# YUMECLOUD TEST ASSIGNMENT**
------------------------

**## О процессе работы**
------------------------



**### Технологии**
------------------
- Python 3
- Django
- Django REST Framework
- PostgreSQL
- Docker и Docker Compose


**### API**

------------------------

/api/orders/ - просмотр всех заказов

/api/orders/{pk}/ - детали конкретного заказа

/api/orders/{pk}/products/ - детали заказа со всеми продуктами

/api/orders/{pk}/products/{pk} - детали продукта в конкретном заказе


/api/products/ - просмотр всех продуктов

/api/products/{pk}/ - детали конкретного продукта

/api/products-availability/ - для получения списк товаров с свободными периодами данных (статистика)

/api/products-rental-sum/ - для получения списка товаров с суммой по аренде (статистика)



**### Запуск**
------------------------
Пропишите следующие команды по порядку в терминал:

git clone https://github.com/salkynbekov/yumecloud.git

cd rental_management/

docker-compose up --build

Далее зайдите в Docker Desktop, перейдите в контейнер django_app и перейдите во вкладку 'Exec'
пропишите следующие команды

python manage.py migrate

python manage.py loaddata fixtures/rental_data.json
