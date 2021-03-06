# foodgram API

## Описание foodram
На этом сервисе пользователи смогут публиковать рецепты, подписываться 
на публикации других пользователей, добавлять понравившиеся рецепты 
в список «Избранное», а перед походом в магазин скачивать сводный 
список продуктов, необходимых для приготовления одного 
или нескольких выбранных блюд.

### Алгоритм авторизации пользователей
Используется аутентификация по токену с [djoiser](https://djoser.readthedocs.io/en/latest/index.html)

Все запросы от имени пользователя должны выполняться с заголовком "Authorization: Token TOKENVALUE"

### Админка
Доступна пользователю с правами администратора (is_staff)

### Workflows
Проект доступен для запуска в деплой с GitHub workflow

Инструкция в [workflow](/WORKFLOW.md)

### Ресурсы API
Ресурсы описаны в [redoc](https://just-eat-it.ru/api/docs/): указаны эндпойнты, разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.

### You can test API [just-eat-it.ru/api](https://just-eat-it.ru/api/) and site [just-eat-it.ru](https://just-eat-it.ru/)

![foodgram workflow](https://github.com/smart5678/foodgram-project-react/actions/workflows/main.yml/badge.svg)
