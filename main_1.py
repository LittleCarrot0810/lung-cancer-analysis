import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ===== Cấu hình trang =====
st.set_page_config(
    page_title="Lung Cancer in the world",
    page_icon="📊",
    layout="wide",
)

API_URL = "https://lung-cancer-analysis-sb24.onrender.com/"

st.sidebar.title("Menu")
lua_chon = st.sidebar.selectbox(
    "Chọn mục",
    ["Selection","General","Age", "Gender", "Smoking", "Yellow Fingers",]
)

# ===== Hiển thị nội dung ban đầu =====
if lua_chon == "Selection":
    st.title("Lung Cancer Data")
    st.subheader("Welcome")

# ===== Lựa chọn thông tin chung =====
elif lua_chon == "General":
    st.subheader("Phân tích dữ liệu ung thư phổi")
    phan_hoi = requests.get(
        f"{API_URL}benhnhan"
    )

    du_lieu = pd.DataFrame(
        phan_hoi.json([])
    )

    st.dataframe(
        du_lieu,
        use_container_width=True
    )

    # Thêm bệnh nhân

    if "show_form" not in st.session_state:
        st.session_state.show_form = False

    if st.button("➕ Thêm bệnh nhân"):
        st.session_state.show_form = True

    if st.session_state.show_form:

        st.subheader("Thêm bệnh nhân")
        so_thu_tu = len(du_lieu) + 1
        st.write(f"Mã bệnh nhân: {so_thu_tu}")
        
        gioi_tinh = st.selectbox(
            "Giới tính",
            ["Male", "Female"]
            )
        
        tuoi = st.number_input(
            "Tuổi", 
            min_value=1, 
            max_value=120
            )
        
        hut_thuoc = st.selectbox(
            "Hút thuốc",
            ["YES", "NO"]
            )

        ngon_tay_vang = st.selectbox(
            "Ngón tay vàng",
            ["YES", "NO"]
            )
        
        lo_au = st.selectbox(
            "Lo âu", 
            ["YES", "NO"]
            )
        
        ap_luc_ban_be = st.selectbox(
            "Áp lực bạn bè", 
            ["YES", "NO"]
            )
        
        benh_man_tinh = st.selectbox(
            "Bệnh mãn tính", 
            ["YES", "NO"]
            )
        
        met_moi = st.selectbox(
            "Mệt mỏi", 
            ["YES", "NO"]
            )
        
        di_ung = st.selectbox(
            "Dị ứng", 
            ["YES", "NO"]
            )
        
        kho_khe = st.selectbox(
            "Khò khè", 
            ["YES", "NO"]
            )
        
        uong_ruou = st.selectbox(
            "Uống rượu", 
            ["YES", "NO"]
            )
        
        ho = st.selectbox(
            "Ho", 
            ["YES", "NO"]
            )
        
        kho_tho = st.selectbox(
            "Khó thở", 
            ["YES", "NO"]
            )
        
        kho_nuot = st.selectbox(
            "Khó nuốt", 
            ["YES", "NO"]
            )
        
        dau_nguc = st.selectbox(
            "Đau ngực", 
            ["YES", "NO"]
            )
        

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Lưu bệnh nhân"):

                du_lieu_moi = {
                    "NUMBER": so_thu_tu,
                    "GENDER": gioi_tinh,
                    "AGE": tuoi,
                    "SMOKING": hut_thuoc,
                    "YELLOW_FINGERS": ngon_tay_vang,
                    "ANXIETY": lo_au,
                    "PEER_PRESSURE": ap_luc_ban_be,
                    "CHRONIC_DISEASE": benh_man_tinh,
                    "FATIGUE": met_moi,
                    "ALLERGY": di_ung,
                    "WHEEZING": kho_khe,
                    "ALCOHOL_CONSUMING": uong_ruou,
                    "COUGHING": ho,
                    "SHORTNESS_OF_BREATH": kho_tho,
                    "SWALLOWING_DIFFICULTY": kho_nuot,
                    "CHEST_PAIN": dau_nguc
                }

                try:
                    res = requests.post(f"{API_URL}them", json=du_lieu_moi)

                    if res.status_code == 200:
                        st.success(f"Đã thêm bệnh nhân số {so_thu_tu}")
                    else:
                        st.error(f"Lỗi {res.status_code}")
                        st.write(res.text)
                except Exception as e:
                    st.error(f"Lỗi kết nối API: {e}")

        with col2:
            if st.button("❌ Hủy"):
                st.session_state.show_form = False       
    # ===== TÌm kiếm bệnh nhân theo ID =====
    if st.button("Tìm bệnh nhân"):
        st.session_state.hien_tim = True

    if st.session_state.get("hien_tim", False):

        ma_so = st.number_input(
            "Nhập ID bệnh nhân",
            min_value=1,
            step=1
        )

        if st.button("Tìm"):

            ket_qua = requests.get(
                f"{API_URL}benhnhan/{int(ma_so)}"
            )

            if ket_qua.status_code == 200:

                data = ket_qua.json()

                st.dataframe(
                    pd.DataFrame(
                        data.items(),
                        columns=["Thông tin", "Giá trị"]
                    )
                )

            else:
                st.error("Không tìm thấy bệnh nhân")
     
                    


# ===== Lựa chọn tuổi =====
elif lua_chon == "Age":

    st.subheader("Age of Lung Cancer")
    # ===== Lấy dữ liệu từ API =====
    response_age = requests.get(
        f"{API_URL}age"
    )
    # ===== Kiểm tra phản hồi từ API =====
    if response_age.status_code == 200:

        age = response_age.json()
        # ===== Chuyển dữ liệu từ API về DataFrame ===== 
        df_age = pd.DataFrame({
            "Nhóm tuổi": age["labels"],
            "Số lượng bệnh nhân": age["values"]
        })
        # ===== Vẽ biểu đồ cột =====
        fig = px.bar(
            df_age,
            x="Nhóm tuổi",
            y="Số lượng bệnh nhân",
            title="Số lượng bệnh nhân theo nhóm tuổi"
        )
        # ===== Hiển thị biểu đồ trên Streamlit =====
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.error("Không lấy được dữ liệu từ API")
    if st.button("Tìm hiểu thêm"):
            st.info("""Trong bộ dữ liệu này, phần lớn bệnh nhân ung thư phổi thuộc nhóm tuổi trung niên và cao tuổi.
        Nguy cơ mắc bệnh có xu hướng tăng theo tuổi do tác động tích lũy của các yếu tố như hút thuốc,
        ô nhiễm môi trường, bệnh hô hấp mãn tính và sự suy giảm khả năng phục hồi của tế bào theo thời gian.
        Nhóm tuổi 60–80 chiếm tỷ lệ cao nhất trong dữ liệu. Đây là giai đoạn các yếu tố nguy cơ
        đã tích lũy trong nhiều năm, đặc biệt là hút thuốc lá và các bệnh lý hô hấp mãn tính.
        Vì vậy nguy cơ phát triển ung thư phổi thường cao hơn so với các nhóm tuổi trẻ.
    """)
    
elif lua_chon == "Yellow Fingers":
    st.title("Tình trạng dựa trên ngón tay vàng")
    response_yellow_fingers = requests.get(
        f"{API_URL}yellow_fingers"
    )
    if response_yellow_fingers.status_code == 200:

        yellow_fingers = response_yellow_fingers.json()

        df_yellow_fingers = pd.DataFrame({
            "Tình trạng ngón tay vàng": yellow_fingers["labels"],
            "Số lượng bệnh nhân": yellow_fingers["values"]
        })
        mapping = {
             "YES": "Có",
             "NO": "Không"
        }
        df_yellow_fingers["Tình trạng ngón tay vàng"] = (
            df_yellow_fingers["Tình trạng ngón tay vàng"].replace(mapping)
        )

        fig = px.pie(
            df_yellow_fingers,
            names="Tình trạng ngón tay vàng",
            values="Số lượng bệnh nhân", 
            title="Phân bố tình trạng theo tình trạng ngón tay vàng"
        )        
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    else:
        st.error("Không lấy được dữ liệu từ API")
    if st.button("Tìm hiểu thêm"):
         st.info("""
        Ngón tay vàng thường xuất hiện ở những người hút thuốc lá trong thời gian dài.
        Đây không phải là nguyên nhân trực tiếp gây ung thư phổi nhưng là dấu hiệu cho
        thấy mức độ tiếp xúc với khói thuốc cao. Trong bộ dữ liệu này, nhóm có ngón tay
        vàng xuất hiện nhiều hơn ở các trường hợp mắc ung thư phổi.
    """)


elif lua_chon == "Gender":
    st.title("Tỷ lệ ung thư phổi theo giối tính")
    response_gender = requests.get(
        f"{API_URL}gender"
    )
    if response_gender.status_code == 200:
        gender = response_gender.json()
        df_gender = pd.DataFrame({
            "Giới tính": gender["names"],
            "Số lượng bệnh nhân": gender["values"]
        })
        mapping = {
             "Male": "Nam",
             "Female": "Nữ"
        }
        df_gender["Giới tính"] = (
             df_gender["Giới tính"].replace(mapping)
        )

        fig = px.pie(
            df_gender,
            names="Giới tính",
            values="Số lượng bệnh nhân",
            title="Số lượng bệnh nhân theo Giới tính"
        )
                
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    else:
        st.error("Không lấy được dữ liệu từ API")
    if st.button("Tìm hiểu thêm"):
            st.info("""
        Số lượng người mắc ung thư phổi giữa nam và nữ không có sự chênh lệch quá lớn.
        Kết quả này cho thấy bệnh có thể xuất hiện ở cả hai giới tính khi tồn tại các
        yếu tố nguy cơ như hút thuốc lá, ô nhiễm môi trường hoặc tiền sử bệnh hô hấp.
    """)





elif lua_chon == "Smoking":
    st.title("Tỷ lệ người hút thuốc bị mắc ung thư phổi")
    response_smoking = requests.get(
        f"{API_URL}smoking"
    )
    if response_smoking.status_code == 200:
        smoking = response_smoking.json()
        df_smoking = pd.DataFrame({
            "Hút thuốc": smoking["labels"],
            "Số lượng bệnh nhân": smoking["values"]
    })
        mapping = {
            "YES": "Có hút thuốc",
            "NO": "Không hút thuốc"
        }
        df_smoking["Hút thuốc"] = (
            df_smoking["Hút thuốc"].replace(mapping)
        )
        fig = px.bar(
            df_smoking,
            x="Hút thuốc",
            y="Số lượng bệnh nhân",
            title="Số lượng bệnh nhân theo tình trạng hút thuốc"
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    else:
        st.error("Không lấy được dữ liệu từ API")
    if st.button("Tìm hiểu thêm"):
            st.info("""
        Hút thuốc lá là một trong những yếu tố nguy cơ hàng đầu của ung thư phổi.
        Các chất độc hại trong khói thuốc có thể gây tổn thương tế bào phổi và làm tăng
        khả năng xuất hiện các đột biến dẫn đến ung thư. Trong bộ dữ liệu này,
        người hút thuốc có xu hướng mắc bệnh nhiều hơn người không hút thuốc.
    """)





elif lua_chon == "Race":
    st.title("Biểu đồ phân bố bệnh nhân theo chủng tộc")
    # ===== Lấy dữ liệu từ API =====
    response_race = requests.get(
        "http://127.0.0.1:8000/race"
    )
    # ===== Kiểm tra phản hồi từ API =====
    if response_race.status_code == 200:

        race = response_race.json()

        # ===== Chuyển dữ liệu từ API về DataFrame
        df_race = pd.DataFrame({
            "Chủng tộc" : race["labels"],
            "Số lượng bệnh nhân" : race["values"]
        })
        

        fig = px.bar(
                df_race,
                x="Chủng tộc",
                y="Số lượng bệnh nhân",
                title="Số lượng bệnh nhân theo chủng tộc"
            )
            # ===== Hiển thị biểu đồ trên Streamlit =====
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    else:
        st.error("Không lấy được dữ liệu từ API")


