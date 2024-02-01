import streamlit as st
import pandas as pd
import re

# Hàm tìm kiếm và trích xuất mã số
def extract_code(description):
    if pd.notnull(description):
        # Tìm tất cả các chuỗi phù hợp với mẫu '2300xxx'
        matches = re.findall('2300\d{3}', description)
        # Trả về chuỗi đầu tiên phù hợp hoặc None nếu không có chuỗi nào phù hợp
        return matches[0] if matches else None
    else:
        # Trả về None nếu giá trị không phải là chuỗi
        return None

# Hàm xử lý khi người dùng tải lên file
def process_uploaded_file(uploaded_file):
    # Đọc file vào DataFrame
    df = pd.read_excel(uploaded_file)
    
    # Tạo cột mới 'Code' bằng cách áp dụng hàm extract_code trên cột 'Description'
    df['Code'] = df['Description'].apply(extract_code)
    
    # Hiển thị DataFrame đã được cập nhật
    st.dataframe(df)
    
    # Lưu kết quả vào một tệp Excel mới
    df.to_excel('updated_test_data.xlsx', index=False)
    st.success("Dữ liệu đã được cập nhật và lưu vào tệp 'updated_test_data.xlsx'")

# Tiêu đề ứng dụng
st.title("Ứng dụng Streamlit cho xử lý dữ liệu Excel")

# Nút tải lên file
uploaded_file = st.file_uploader("Chọn một file Excel", type=["xlsx", "xls"])

# Kiểm tra xem người dùng đã tải lên file chưa
if uploaded_file is not None:
    # Xử lý file đã tải lên
    process_uploaded_file(uploaded_file)
