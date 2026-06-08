from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import sqlite3

# ===== Khởi tạo ứng dụng API =====
app = FastAPI()
# ===== Đọc dữ liệu từ file CSV =====
df = pd.read_csv("Lung_Cancer.csv")

# Tạo model dữ liệu
class Benhnhan(BaseModel):
    NUMBER: int
    GENDER: str
    AGE: int
    SMOKING: str
    YELLOW_FINGERS: str
    ANXIETY: str
    PEER_PRESSURE: str
    CHRONIC_DISEASE: str
    FATIGUE: str
    ALLERGY: str
    WHEEZING: str
    ALCOHOL_CONSUMING: str
    COUGHING: str
    SHORTNESS_OF_BREATH: str
    SWALLOWING_DIFFICULTY: str
    CHEST_PAIN: str

# ===== Định nghĩa các endpoint =====


@app.get("/")
def home():
    return {"message": "Data Analysis API"}


# Endpoint 1: Hiển thị dữ liệu
@app.get("/benhnhan")
def lay_danh_sach():

    ket_noi = sqlite3.connect(
        "lung_cancer.db"
    )

    du_lieu = pd.read_sql(
        "SELECT * FROM benh_nhan",
        ket_noi
    )

    ket_noi.close()

    return du_lieu.to_dict(
        orient="records"
    )

# Endpoint 2: Thêm dữ liệu bệnh nhân
@app.post("/them")
def them_benh_nhan(benh_nhan: Benhnhan):

    try:
        ket_noi = sqlite3.connect("lung_cancer.db")
        con_tro = ket_noi.cursor()

        con_tro.execute(
            """
            INSERT INTO benh_nhan
            (
                NUMBER,
                GENDER,
                AGE,
                SMOKING,
                YELLOW_FINGERS,
                ANXIETY,
                PEER_PRESSURE,
                CHRONIC_DISEASE,
                FATIGUE,
                ALLERGY,
                WHEEZING,
                ALCOHOL_CONSUMING,
                COUGHING,
                SHORTNESS_OF_BREATH,
                SWALLOWING_DIFFICULTY,
                CHEST_PAIN
            )
            VALUES
            (
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?
            )
            """,
            (
                benh_nhan.NUMBER,
                benh_nhan.GENDER,
                benh_nhan.AGE,
                benh_nhan.SMOKING,
                benh_nhan.YELLOW_FINGERS,
                benh_nhan.ANXIETY,
                benh_nhan.PEER_PRESSURE,
                benh_nhan.CHRONIC_DISEASE,
                benh_nhan.FATIGUE,
                benh_nhan.ALLERGY,
                benh_nhan.WHEEZING,
                benh_nhan.ALCOHOL_CONSUMING,
                benh_nhan.COUGHING,
                benh_nhan.SHORTNESS_OF_BREATH,
                benh_nhan.SWALLOWING_DIFFICULTY,
                benh_nhan.CHEST_PAIN
            )
        )

        ket_noi.commit()

        return {"message": "Đã thêm bệnh nhân"}

    except Exception as e:
        print("LỖI:", e)
        return {"error": str(e)}

    finally:
        ket_noi.close()

# Endpoint 3: Tìm kiếm theo ID
@app.get("/benhnhan/{ma_so}")
def tim_benh_nhan(ma_so: int):

    ket_noi = sqlite3.connect("lung_cancer.db")

    truy_van = """
    SELECT *
    FROM benh_nhan
    WHERE NUMBER = ?
    """

    du_lieu = pd.read_sql(
        truy_van,
        ket_noi,
        params=(ma_so,)
    )

    ket_noi.close()

    if du_lieu.empty:
        return {"message": "Không tìm thấy"}

    return du_lieu.iloc[0].to_dict()


# Endpoint 4: Nhóm tuổi nguy cơ cao mắc ung thư phổi
@app.get("/age")
def age_chart():

    temp_df = df.copy()

    khoang_tuoi = [20, 40, 60, 80, 100]
    ten_khoang = ["20-40", "40-60", "60-80", "80-100"]

    temp_df["nhom_tuoi"] = pd.cut(
        temp_df["AGE"],
        bins=khoang_tuoi,
        labels=ten_khoang
    )

    age_chart = (
        temp_df["nhom_tuoi"]
        .value_counts()
        .sort_index()
    )

    return {
        "labels": age_chart.index.tolist(),
        "values": age_chart.values.tolist()
    }

# Endpoint 5: Tỷ lệ mắc ung thư phổi theo giới tính
@app.get("/gender")
def gender_chart():

    gender_chart = df["GENDER"].value_counts()

    return {
        "names": gender_chart.index.tolist(),
        "values": gender_chart.values.tolist()
    }


# Endpoint 4: Phân loại bệnh nhân theo tình trạng dùng thuốc
@app.get("/smoking")
def smoking_chart():
    
    smoking_chart = df["SMOKING"].value_counts()

    return {
        "labels": smoking_chart.index.tolist(),
        "values": smoking_chart.tolist()
    }

# Endpoint 5: Phân loại theo tình trạng ngón tay đổi màu do hút thuốc
@app.get("/yellow_fingers")
def yellow_finger_chart():

    yellow_finger_chart = df["YELLOW_FINGERS"].value_counts()

    return {
        "labels": yellow_finger_chart.index.tolist(),
        "values": yellow_finger_chart.values.tolist()
    }

# Endpoint 6: Phân loại theo tình trạng lo âu
@app.get("/anxiety")
def anxiety_chart():

    anxiety_chart = df["ANXIETY"].value_counts()

    return {
        "labels" : anxiety_chart.index.tolist(),
        "values" : anxiety_chart.values.tolist()
    }

# Endpoint 7: Phân loại theo áp lực từ xã hội
@app.get("/peer_pressure")
def peer_pressure_chart():

    peer_pressure_chart = df["PEER_PRESSURE"].value_counts()

    return {
        "labels" : peer_pressure_chart.index.tolist(),
        "values" : peer_pressure_chart.values.tolist()
    }

# Endpoint 8: Phân loại theo bệnh mãn tính
@app.get("/chronic_disease")
def chronic_disease_chart():

    chronic_disease_chart = df["CHRONIC_DISEASE"].value_counts()

    return {
        "labels" : chronic_disease_chart.index.tolist(),
        "values" : chronic_disease_chart.values.tolist()
    }

# Endpoint 9: Dấu hiệu mệt mỏi
@app.get("/fatigue")
def fatigue_chart():

    fatigue_chart = df["FATIGUE"].value_counts()

    return {
        "labels" : fatigue_chart.index.tolist(),
        "values" : fatigue_chart.values.tolist()
    }

# Endpoint 10: Dấu hiệu dị ứng
@app.get("/allergy")
def allergy_chart():

    allergy_chart = df["ALLERGY"].value_counts()

    return {
        "labels" : allergy_chart.index.tolist(),
        "values" : allergy_chart.values.tolist()
    }

# Endpoint 11: Dấu hiệu khó thở
@app.get("/wheezing")
def wheezing_chart():

    wheezing_chart = df["WHEEZING"].value_counts()

    return {
        "labels" : wheezing_chart.index.tolist(),
        "values" : wheezing_chart.values.tolist()
    }

# Endpoint 12: Tiền sử sử dụng rượu bia
@app.get("/alcohol_consuming")
def alcohol_consuming_chart():

    alcohol_consuming_chart = df["ALCOHOL_CONSUMING"].value_counts()

    return {
        "labels" : alcohol_consuming_chart.index.tolist(),
        "values" : alcohol_consuming_chart.values.tolist()
    }

# Endpoint 13: Dấu hiệu ho
@app.get("/coughing")
def coughing_chart():

    coughing_chart = df["COUGHING"].value_counts()

    return {
        "labels" : coughing_chart.index.tolist(),
        "values" : coughing_chart.values.tolist()
    }

# Endpoint 14: Dấu hiệu khó thở
@app.get("/shortness_of_breath")
def shortness__of_breath_chart():

    shortness__of_breath_chart = df["SHORTNESS_OF_BREATH"].value_counts()

    return {
        "labels" : shortness__of_breath_chart.index.tolist(),
        "values" : shortness__of_breath_chart.values.tolist()
    }

# Endpoint 15: Dấu hiệu khó nuốt
@app.get("/swallowung_difficulty")
def swallowing_difficuly_chart():

    swallowing_difficuly_chart = df["SWALLOWING_DIFFICULTY"].value_counts()

    return {
        "labels" : swallowing_difficuly_chart.index.tolist(),
        "values" : swallowing_difficuly_chart.values.tolist()
    }

# Endpoint 16: Dấu hiệu đau ngực
@app.get("/chest_pain")
def chest_pain_chart():

    chest_pain_chart = df["CHEST_PAIN"].value_counts()

    return {
        "labels" : chest_pain_chart.index.tolist(),
        "values" : chest_pain_chart.values.tolist()
    }


