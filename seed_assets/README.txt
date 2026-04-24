ParkNet — локальные фото для заполнения БД
==========================================

Положите файлы в эту папку (рядом с manage.py: backend/seed_assets/).

Поддерживаются расширения: .jpg .jpeg .png .webp (регистр имени файла — нижний).

1) parks/  — большие «герой»-фото для карточек парков (горизонтально, ~1200×800 или 16:9, до ~2 МБ).
   Имена файлов (без расширения = slug парка):
   - central-park
   - silverwood-park
   - oak-creek-path

   Что найти: виды парка, аллеи, газоны, город на фоне — как в макете Central Park.

2) projects/ — миниатюры для блока «Weekly improvements» (~600×400 или квадрат 600×600).
   - north-park-reforestation → проект «North Park Reforestation»
   - trail-lighting-upgrade    → проект «Trail Lighting Upgrade»

   Что найти: посадка деревьев / саженцы; парковые фонари или работы по освещению.

3) reports/ — фото для демо-отчётов (достаточно ~800 px по длинной стороне).
   - broken-bench      → «сломанная скамейка», статус IN PROGRESS, парк Silverwood
   - graffiti-cleaned  → «граффити убрали», статус RESOLVED, парк Oak Creek

   Что найти: повреждённая скамейка; чистая стена/тропа после уборки (или до/после).

Команда:  python manage.py seed_demo_media

Пользователь для демо-отчётов: parknet_demo / пароль demo12345 (создаётся командой).
