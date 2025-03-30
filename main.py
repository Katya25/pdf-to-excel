from flask import Flask, render_template, request, send_file
import fitz  # PyMuPDF
import re
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files["pdf"]

        if uploaded_file.filename.endswith(".pdf"):
            # Сохраняем PDF во временный файл
            temp_pdf_path = "temp_input.pdf"
            uploaded_file.save(temp_pdf_path)

            # Открываем PDF
            doc = fitz.open(temp_pdf_path)
            full_text = "\n".join(page.get_text() for page in doc)
            patient_blocks = re.split(r"\bВ И П И С К А\b", full_text)[1:]

            patients = []
            for block in patient_blocks:
                data = {}
                match = re.search(
                    r"із медичної карти стаціонарного хворого №\s*(\d+)",
                    block)
                data["Номер виписки"] = match.group(
                    1).strip() if match else None

                match = re.search(
                    r"Прізвище, ім’я, по батькові хворого\s+([А-ЯІЇЄа-яіїє'\- ]+)",
                    block)
                data["ПІБ"] = match.group(1).strip() if match else None

                match = re.search(
                    r"Дата народження\s+(\d)\s+(\d)\s+(\d)\s+(\d)\s+(\d)\s+(\d)",
                    block)
                if match:
                    day = match.group(1) + match.group(2)
                    month = match.group(3) + match.group(4)
                    year_part = int(match.group(5) + match.group(6))
                    year = 1900 + year_part if year_part > 25 else 2000 + year_part
                    birth_date_str = f"{day.zfill(2)}.{month.zfill(2)}.{year}"
                    data["Дата народження"] = birth_date_str
                    try:
                        birth_date = datetime.strptime(birth_date_str,
                                                       "%d.%m.%Y")
                        today = datetime.today()
                        age = today.year - birth_date.year - (
                            (today.month, today.day)
                            < (birth_date.month, birth_date.day))
                        data["Вік"] = age
                    except:
                        data["Вік"] = None
                else:
                    data["Дата народження"] = None
                    data["Вік"] = None

                match = re.search(
                    r"(креатин[іi]н(?:[\s\S]{0,100}?))([\d]+[.,]?\d*)", block,
                    re.IGNORECASE)
                creatinine = match.group(2).replace(",",
                                                    ".") if match else None
                data["Креатинін"] = creatinine

                gender = "Невідомо"
                if data["ПІБ"]:
                    parts = data["ПІБ"].split()
                    if len(parts) >= 3:
                        patronymic = parts[2]
                        if patronymic.endswith("ич"):
                            gender = "Чол"
                        elif patronymic.endswith("а"):
                            gender = "Жін"
                        else:
                            gender = "Чол"
                data["Стать"] = gender

                try:
                    if creatinine and data["Вік"] and gender in ["Чол", "Жін"]:
                        scr = float(creatinine) / 88.4
                        age = data["Вік"]
                        if gender == "Жін":
                            k = 0.7
                            alpha = -0.241
                            female_factor = 1.012
                        else:
                            k = 0.9
                            alpha = -0.302
                            female_factor = 1.0

                        scr_k = scr / k
                        egfr = 142 * min(scr_k, 1)**alpha * max(
                            scr_k, 1)**-1.200 * 0.9938**age * female_factor
                        data["ШКФ"] = round(egfr)
                    else:
                        data["ШКФ"] = None
                except:
                    data["ШКФ"] = None

                patients.append(data)

            df = pd.DataFrame(patients)
            df.sort_values(by=["Креатинін"], ascending=False, inplace=True)
            df = df.drop_duplicates(subset=["ПІБ", "Дата народження"],
                                    keep="first")

            output_path = "final_output.xlsx"
            df.to_excel(output_path, index=False)

            return send_file(output_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
