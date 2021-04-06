![yamdb workflow](https://github.com/mishastik78/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Учебный проект

Данный проект предназначен для взаимодействия c Django через API с использованием виртуализации средств разработки Docker

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Docker
Docker-compose

### Installing

Для запуска приложения введите

```
docker-compose up
```

После завершения установки приложение доступно на порту 8000

Для создания суперпользователя используйте команду

```
python manage.py createsuperuser
```
в коммандной строке контейнера web.

Для загрузки тестовых данных введите в коммандной строке контейнера web

```
python manage.py loaddata fixtures.json
```


## Authors

* **Mikhail Indurov**

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
