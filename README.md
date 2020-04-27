## Django API Chat

### Описание 

Джанго приложение для чата. Предоставляет модели и апи для создания/просмотра 
чатов. Подразумевается, что сам чаттинг будет реализован на другом сервисе. 
Например на вебсокетах aiohttp.

### Возможности
- Диалог
- Групповой чат
- Сообщение прочитано/не прочитано


### Установка

1. Добавить "chat" в INSTALLED_APPS:
```python3
INSTALLED_APPS = [
        ...
        'chat',
]
```

2. Подключить chat.router в проект:
```python3
from django.urls import include, path
from chat.router import router

urlpatterns = [
    path('api/', include(router.urls)),
]
```

3. Запустить миграции:
```shell script
python manage.py migrate
```
