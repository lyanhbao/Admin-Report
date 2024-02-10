import streamlit as st
import pandas as pd
import re
import base64

# Hàm tìm kiếm và trích xuất mã số
def extract_code(description, pattern):
    if pd.notnull(description):
        matches = re.findall(pattern, description)
        return matches[0] if matches else None
    else:
        return None

def process_file(file, pattern, output_name):
    # Read the file into a DataFrame
    df = pd.read_excel(file)

    # Apply the extract_code function
    df['Code'] = df['Description'].apply(lambda desc: extract_code(desc, pattern))

    # Save to a new Excel file
    df.to_excel(output_name, index=False)

    return df

def main():
    st.title("Code Extractor App")

    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        # Dropdown for pattern selection
        pattern_option = st.selectbox("Select the pattern year:", ["2023", "2024"])

        # Mapping pattern options to actual regex patterns
        pattern_mapping = {"2023": r'2300\d{3}', "2024": r'2400\d{3}'}
        pattern = pattern_mapping[pattern_option]

        output_name = st.text_input("Enter the output file name:", "output.xlsx")

        if st.button("Process"):
            df_result = process_file(uploaded_file, pattern, output_name)
            st.dataframe(df_result)

            st.success(f"File processed successfully. Download your result: [{output_name}]")
            st.markdown(get_binary_file_downloader_html(output_name), unsafe_allow_html=True)

def get_binary_file_downloader_html(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/xlsx;base64,{b64}" download="{file_path}">Download {file_path}</a>'
    return href

def main():
    st.markdown("""
    <style>
    body { 
        background-color: #f0f5f9; /* Soft background color */
        font-family: 'Arial', sans-serif;
    }
    .stButton > button { 
        background-color: #007bff; /* Blue button */
        color: white;
        border: none;  /* Optional: Remove default border */
        padding: 10px 20px; /* Adjust padding to your liking */
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Code Extractor App")
    # ... (rest of your main function's code)

if __name__ == "__main__":
    main()
