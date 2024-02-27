import streamlit as st
import pandas as pd
import csv
from io import StringIO
import base64
import re  # Import the regex module

def split_and_convert_data(input_files):
    merged_df = pd.DataFrame()

    for uploaded_file in input_files:
        content = uploaded_file.getvalue().decode('utf-8')
        stringio = StringIO(content)
        reader = csv.reader(stringio)

        rows = list(reader)

        if "Product" in rows[8]:
            merged_df = process_case_1(uploaded_file, rows, merged_df)
        else:
            merged_df = process_case_2(uploaded_file, rows, merged_df)

    # Automatically detect the pattern year
    pattern = detect_pattern_year(merged_df['Description'])

    # Apply the extract_code function to merged_df
    merged_df['Code'] = merged_df['Description'].apply(lambda desc: extract_code(desc, pattern))
    return merged_df


def detect_pattern_year(descriptions):
    for description in descriptions:
        matches_2023 = re.findall(r'2300\d{3}', description)
        matches_2024 = re.findall(r'2400\d{3}', description)
        if matches_2023:
            return '2023'
        elif matches_2024:
            return '2024'
    # Default to 2023 if no matches found
    return '2023'


def extract_code(description, pattern):
    if pd.notnull(description):
        matches = re.findall(rf'{pattern}(\d{{3}})', description)
        return matches[0] if matches else None
    else:
        return None


def process_case_1(uploaded_file, rows, merged_df):
    split_index = 0
    count_empty_lines = 0
    for idx, row in enumerate(rows):
        if not row:
            count_empty_lines += 1
            if count_empty_lines == 2:
                split_index = idx + 1
                break

        header = [
            "Bill to","Invoice number","Invoice date", "Due Date",  
            "Billing ID", "Currency", "Invoice amount", "",
            "Product"
        ]

        new_data = [header]
        new_data.append([
            rows[0][1],
            rows[1][1],
            rows[2][1],
            rows[3][1],
            rows[4][1],
            rows[5][1],
            rows[6][1],
            "",
            rows[8][1]
        ])

        df2 = pd.DataFrame(rows[split_index:], columns=["Order name", "Purchase Order", "Description", "Quantity", "UOM", "Amount"])
        df2 = df2.dropna(subset=['Order name'])
        df2 = df2[df2['Order name'] != 'Order name']
        df2.reset_index(drop=True, inplace=True)
        df2['source_name'] = uploaded_file.name

        new_data_df = pd.DataFrame(new_data[1:], columns=new_data[0])
        new_data_df['source_name'] = uploaded_file.name
        new_data_df = new_data_df.dropna(subset=['Billing ID'])

        merged_df = pd.concat([merged_df, new_data_df.merge(df2, on='source_name', how='right')], ignore_index=True)
        merged_df = merged_df.dropna(subset=['Description'])
        merged_df = merged_df.drop_duplicates()
    return merged_df

def process_case_2(uploaded_file, rows, merged_df):
    split_index = 0
    count_empty_lines = 0
    for idx, row in enumerate(rows):
        if not row:
            count_empty_lines += 1
            if count_empty_lines == 2:
                split_index = idx + 1
                break

    header = [
        "Bill to", "Invoice number", "Invoice date","Due Date", "Billing ID",
        "Currency", "Invoice amount", "", "Product"
    ]

    new_data = [header]
    new_data.append([
        rows[0][1],
        rows[1][1],
        rows[2][1],
        None,
        rows[3][1],
        rows[4][1],
        rows[5][1],
        "",
        rows[7][1]
    ])

    df2 = pd.DataFrame(rows[split_index:], columns=["Order name", "Purchase Order", 
    "Description", "Quantity", "UOM", "Amount"])
    df2 = df2.dropna(subset=['Order name'])
    df2 = df2[df2['Order name'] != 'Order name']
    df2.reset_index(drop=True, inplace=True)
    df2['source_name'] = uploaded_file.name

    new_data_df = pd.DataFrame(new_data[1:], columns=new_data[0])
    new_data_df['source_name'] = uploaded_file.name
    new_data_df = new_data_df.dropna(subset=['Billing ID'])

    merged_df = pd.concat([merged_df, new_data_df.merge(df2, on='source_name', how='inner')], ignore_index=True)
    merged_df = merged_df.dropna(subset=['Description'])
    merged_df = merged_df.drop_duplicates()
    return merged_df


def main():
    st.title("Multiple CSV Files Merger and Converter")

    uploaded_files = st.file_uploader("Upload multiple CSV files", type="csv", accept_multiple_files=True)
    if uploaded_files:
        st.write("Files successfully uploaded.")

        merged_df = split_and_convert_data(uploaded_files)

        # Display the merged DataFrame
        st.write("Merged Data:")
        st.write(merged_df)

        # Download link for the merged data
        st.markdown(get_csv_download_link(merged_df), unsafe_allow_html=True)

        output_name = st.text_input("Enter the output file name:", "output.xlsx")

        if st.button("Process"):
            df_result = process_file(uploaded_file, merged_df)
            st.dataframe(df_result)

            st.success(f"File processed successfully. Download your result: [{output_name}]")
            st.markdown(get_binary_file_downloader_html(output_name), unsafe_allow_html=True)


def process_file(file, df):
    # Automatically detect the pattern year
    pattern = detect_pattern_year(df['Description'])

    # Apply the extract_code function
    df['Code'] = df['Description'].apply(lambda desc: extract_code(desc, pattern))

    # Save to a new Excel file
    df.to_excel(output_name, index=False)

    return df


def get_csv_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode('utf-8')).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="merged_data.csv">Download Merged Data</a>'
    return href


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{bin_file}">Download {file_label}</a>'
    return href


if __name__ == "__main__":
    main()
