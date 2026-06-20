# Morning Paper — Личный кабинет (Next.js)

Веб-кабинет поверх FastAPI-бэкенда (`src/morning_paper/api`). Тонкий клиент: вся
логика — на бэкенде, кабинет лишь вызывает REST `/v1/...`.

## Страницы

| Маршрут | Что делает | API |
|---|---|---|
| `/` | Обзор: настройки, профиль, последние выпуски | `GET /v1/users/{id}`, `/profile`, `/issues` |
| `/settings` | Язык, стиль, таймзона, доставка | `PUT /v1/users/{id}` |
| `/sources` | Каталог источников + конфиг на пользователя | `GET /v1/sources`, `GET/PUT …/sources/{sid}` |
| `/themes` | Галерея стилей, выбор | `GET /v1/themes`, `PUT /v1/users/{id}` |
| `/profile` | Темы/сущности, построение, 👍/👎 | `…/profile`, `…/profile:build`, `…/feedback` |
| `/issues` | Сборка выпуска + история, PDF | `POST …/issues`, `GET /v1/issues/{id}` |
| `/privacy` | Экспорт/удаление данных (GDPR/CCPA) | `GET …/data:export`, `DELETE …/data` |

Текущий пользователь хранится в `localStorage` (`mp_user`, по умолчанию `me`) и
шлётся в заголовке `X-MP-User` — это first-party авторизация бэкенда. Переключатель
пользователя — в правом верхнем углу.

## Запуск (dev)

```bash
# 1) бэкенд (из корня репозитория)
pip install -e ".[api]"
morning-paper init-db          # опционально: история выпусков
morning-paper serve            # FastAPI на :8000

# 2) кабинет
cd cabinet
cp .env.example .env.local     # при необходимости поменяйте API_PROXY_TARGET
npm install
npm run dev                    # http://localhost:3000
```

Браузер ходит только в свой origin: `/api/*` проксируется на бэкенд
(`next.config.mjs`), поэтому CORS не нужен. На бэкенде CORS для `localhost:3000`
всё же включён по умолчанию (переопределяется `MP_CORS_ORIGINS`), если решите
ходить в API напрямую.

## Сборка

```bash
npm run build        # типчек + production-сборка
npm run start        # production-сервер
```
