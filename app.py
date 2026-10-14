import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# --- DỮ LIỆU GỐC ---
data = {
    "Ho_va_ten": [
        "Trần Thị Khánh Linh",
        "Nguyễn Ngọc Thu Ngân",
        "Đào Đức Dũng",
        "Nguyễn Viết Việt",
        "Trần Thành Nam",
        "Nguyễn Đình Kiệt",
        "Mai Thị Huệ",
        "Đoàn Khánh Duy",
        "Nguyễn Trọng Tấn",
        "Nguyễn Khánh Duy",
    ],
    "Chuyên_can": [9.0, 7.5, 6.8, 6.9, 8.5, 9.5, 8.3, 8.8, 9.2, 9.6],
    "Giua_ki": [8.8, 7.6, 9.4, 9.2, 8.7, 9.4, 7.8, 7.5, 7.9, 8.2],
    "Cuoi_ki": [9.3, 7.9, 8.4, 9.5, 8.2, 7.8, 9.4, 7.5, 8.2, 6.1],
    "Tong_ket": [9.09, 7.73, 8.38, 8.89, 8.41, 8.62, 8.70, 7.76, 8.31, 7.43],
    "Xep_loai": [
        "Giỏi",
        "Khá",
        "Khá",
        "Giỏi",
        "Khá",
        "Giỏi",
        "Giỏi",
        "Khá",
        "Khá",
        "Khá",
    ],
}

df = pd.DataFrame(data)

# --- GIAO DIỆN STREAMLIT ---

# 1. Tiêu đề ứng dụng
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 2. Hiển thị bảng điểm của 10 sinh viên
st.subheader("📋 Bảng điểm chi tiết của 10 sinh viên")
st.dataframe(df, use_container_width=True)

# 3. Tính toán các chỉ số thống kê
diem_tb_lop = df["Tong_ket"].mean()

max_row = df.loc[df["Tong_ket"].idxmax()]
min_row = df.loc[df["Tong_ket"].idxmin()]

# Số sinh viên đạt (giả định điểm tổng kết >= 5.0 là đạt)
so_sv_dat = len(df[df["Tong_ket"] >= 5.0])

# Hiển thị các thông tin thống kê chung
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="📊 Điểm trung bình cả lớp", value=f"{diem_tb_lop:.2f}"
    )
with col2:
    st.metric(label="🏆 Điểm tổng kết cao nhất", value=f"{max_row['Tong_ket']}")
    st.caption(f"({max_row['Ho_va_ten']})")
with col3:
    st.metric(label="⚠️ Điểm tổng kết thấp nhất", value=f"{min_row['Tong_ket']}")
    st.caption(f"({min_row['Ho_va_ten']})")

st.info(f"✨ Số lượng sinh viên đạt yêu cầu: **{so_sv_dat}/10** sinh viên")

st.markdown("---")

# 4. Danh sách xổ xuống để chọn sinh viên và xem thông tin chi tiết
st.subheader("🔍 Tra cứu thông tin cá nhân sinh viên")
selected_student = st.selectbox(
    "Chọn họ tên sinh viên:", df["Ho_va_ten"].tolist()
)

# Lọc thông tin sinh viên được chọn
student_info = df[df["Ho_va_ten"] == selected_student].iloc[0]

sc1, sc2, sc3, sc4, sc5 = st.columns(5)
sc1.metric("Chuyên cần", f"{student_info['Chuyên_can']}")
sc2.metric("Giữa kỳ", f"{student_info['Giua_ki']}")
sc3.metric("Cuối kỳ", f"{student_info['Cuoi_ki']}")
sc4.metric("Tổng kết", f"{student_info['Tong_ket']}")
sc5.metric("Xếp loại", f"{student_info['Xep_loai']}")

st.markdown("---")

# 5. Hiển thị biểu đồ cột điểm tổng kết của 10 sinh viên (chỉ lấy tên riêng cho gọn)
st.subheader("📊 Biểu đồ trực quan điểm tổng kết")

# Lấy tên riêng (từ cuối cùng) cho trục y
short_names = [name.split()[-1] for name in df["Ho_va_ten"]]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(short_names, df["Tong_ket"], color="#6495ED")

ax.set_xlabel("Điểm tổng kết", fontsize=11)
ax.set_ylabel("Tên sinh viên", fontsize=11)
ax.set_title(
    "Biểu đồ cột thể hiện điểm tổng kết của 10 sinh viên",
    fontsize=13,
    fontweight="bold",
)
ax.set_xlim(0, 10)
ax.invert_yaxis()  # Đảo ngược để sinh viên đầu bảng hiển thị lên trên

# Hiển thị giá trị số trực tiếp trên các thanh cột
for bar in bars:
    width = bar.get_width()
    ax.text(
        width + 0.1,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.2f}",
        va="center",
        ha="left",
        fontsize=9,
    )

st.pyplot(fig)

# 6. Thông tin người tạo ứng dụng ở chân trang (chữ nhỏ)
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 12px;'>"
    "Người tạo ứng dụng: [Lê Thị Ánh Dương] - MSSV: [038308000151]"
    "</p>",
    unsafe_allow_html=True,
)