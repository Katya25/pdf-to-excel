# 🩺 PDF to Excel (Flask App for Ukrainian Medical Discharge Summaries)

This repository contains a Flask-based web application that allows users to upload Ukrainian medical discharge summaries in PDF format and automatically extract patient data into an Excel spreadsheet.

📌 **Note:** The application is designed specifically for the structure of discharge summaries used in Ukraine. Therefore, the detailed documentation below is provided in Ukrainian and Russian.

---

## 🧩 Функціональність

Цей додаток автоматично:

- Витягує **ПІБ**, **номер виписки**, **дату народження**, **вік**, **рівень креатиніну**
- Визначає **стать** пацієнта за по батькові
- Обчислює **ШКФ (швидкість клубочкової фільтрації)** за формулою CKD-EPI 2021
- Формує **Excel-файл** з усіма даними
- Автоматично **прибирає дублікати**
- Працює як **локально**, так і через вебсайт

---

## 🌐 Онлайн версія

Готовий сайт працює постійно за адресою:

🔗 **https://pdf-to-excel-1-e73d.onrender.com**

Ти можеш завантажити PDF — і одразу отримаєш Excel-файл.

---

## ⚙️ Як запустити локально?

> **📌 Увага:** адреса сайту у вас буде своя! Після запуску шукайте її в консолі (рядок типу `Running on http://127.0.0.1:5000` або `http://127.0.0.1:3000`)

### 🪄 Кроки:

1. **Клонуй репозиторій**:
   ```bash
   git clone https://github.com/Katya25/pdf-to-excel.git
   cd pdf-to-excel
   ```

2. **Створи віртуальне середовище**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Встанови залежності**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Запусти Flask-додаток**:
   ```bash
   python3 main.py
   ```

5. **Відкрий сайт у браузері**:
   Залежно від повідомлення в консолі:
   ```
   http://127.0.0.1:5000
   ```
   або
   ```
   http://127.0.0.1:3000
   ```

> ✅ Якщо все зроблено правильно — побачиш вікно для завантаження PDF.

---

💙 Зроблено з турботою

Цей проєкт було створено на прохання лікаря з України, який щодня працює з великим обсягом медичних виписок.
Я щиро рада мати змогу допомогти медикам — людям, які щодня рятують життя.

🩺 Якщо цей інструмент хоч трохи спрощує їхню роботу — значить, усе було недаремно.
Завжди рада бути корисною! 💫
