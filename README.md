# Проект парсинга pep

## Описание проекта

Этот проект представляет собой многофункциональный парсер документации Python, который включает:

1. Парсер нововведений в версиях Python (`whats-new`)
2. Парсер последних версий Python (`latest-versions`)
3. Загрузчик документации (`download`)
4. Парсер документов PEP (`pep`)

## Основные функции

### 1. Режим `whats-new`
Парсит информацию о нововведениях в различных версиях Python:
- Ссылки на статьи
- Заголовки версий
- Редакторов и авторов

Пример вывода:
```
https://docs.python.org/3/whatsnew/3.13.html What's New In Python 3.13 Editors: Adam Turner and Thomas Wouters
https://docs.python.org/3/whatsnew/3.12.html What's New In Python 3.12 Editor: Adam Turner
```

### 2. Режим `latest-versions`
Получает информацию о доступных версиях Python:
- Ссылки на документацию
- Номера версий
- Статусы версий

Пример вывода:
```
https://docs.python.org/3.14/ 3.14 in development
https://docs.python.org/3.13/ 3.13 stable
https://docs.python.org/3.12/ 3.12 security-fixes
```

### 3. Режим `download`
Загружает архив с документацией Python в формате PDF:
- Автоматически определяет последнюю версию
- Сохраняет архив в папку `downloads`
- Логирует процесс загрузки

Пример лога:
```
21.04.2025 20:07:51 - [INFO] - Архив был загружен и сохранён: C:\Dev\bs4_parser_pep\src\downloads\python-3.13-docs-pdf-a4.zip
```

### 4. Режим `pep`
Анализирует документы PEP (Python Enhancement Proposals):
- Собирает статистику по статусам PEP
- Сравнивает статусы между общим списком и страницами PEP
- Формирует отчет в CSV формате
- Логирует несоответствия статусов

## Использование

```bash
python src/main.py [режим] [опции]
```

Доступные режимы:
- `whats-new` - нововведения в версиях Python
- `latest-versions` - информация о версиях Python
- `download` - загрузка документации
- `pep` - анализ документов PEP

Опции:
- `-c/--clear-cache` - очистка кеша
- `-o/--output {pretty,file}` - формат вывода (таблица или файл)

## Примеры команд

1. Получить информацию о нововведениях:
```bash
python src/main.py whats-new -o pretty
```

2. Получить информацию о версиях Python:
```bash
python src/main.py latest-versions -o file
```

3. Загрузить документацию:
```bash
python src/main.py download
```

4. Проанализировать PEP:
```bash
python src/main.py pep -o file
```

## Структура проекта

```
bs4_parser_pep/
├── src/
│   ├── __init__.py
│   ├── configs.py       # Конфигурации парсера
│   ├── constants.py     # Константы проекта
│   ├── exceptions.py    # Пользовательские исключения
│   ├── main.py          # Основной скрипт
│   ├── outputs.py       # Функции вывода
│   └── utils.py         # Вспомогательные функции
├── downloads/           # Загруженные архивы
├── logs/                # Логи работы
│   └── parser.log
├── results/             # Результаты работы
│   └── pep_results.csv
├── tests/               # Тесты
├── .flake8              # Конфигурация линтера
├── .gitignore
├── pytest.ini           # Конфигурация тестов
├── README.md
└── requirements.txt     # Зависимости
```

## Логирование

Все действия парсера записываются в файл `logs/parser.log` в формате:
```
[дата-время] - [уровень] - [сообщение]
```

Пример:
```
21.04.2025 20:04:09 - [INFO] - Парсер запущен!
```

## Требования

- Python 3.8+
- Установленные зависимости из `requirements.txt`

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Viocid/bs4_parser_pep.git
cd bs4_parser_pep
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Тестирование

Для запуска тестов:
```bash
pytest
```