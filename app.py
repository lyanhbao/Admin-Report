import streamlit as st
import pandas as pd
import csv
from io import StringIO
import base64
import re  # Import the regex module
from openpyxl.utils.exceptions import IllegalCharacterError

def classify_file_type(rows):
    if "Product" in rows[7] and rows[7][1] == "Display and Video 360":
        return "DV 360 - Case 2"
    elif "Product" in rows[7] and rows[7][1] == "Google Ads":
        return "Google Ads case 2"
    elif "Product" in rows[7] and rows[7][1] == "Campaign Manager 360":
        return "CM360 case 2"
    elif "Product" in rows[7] and rows[7][1] == "YouTube Reservation":
        return "YouTube Reservation case 2"
    elif rows[8][1] == "Display and Video 360":
        return "DV 360 - Case 1"
    elif rows[8][1] == "Google Ads":
        return "Google Ads"
    elif rows[8][1] == "Campaign Manager 360":
        return "CM360"
    elif rows[8][1] == "YouTube Reservation":
        return "YouTube Reservation"
    else:
        return "Unknown"

def split_and_convert_data(input_files):
    merged_df = pd.DataFrame()

    for uploaded_file in input_files:
        content = uploaded_file.getvalue().decode('utf-8')
        stringio = StringIO(content)
        reader = csv.reader(stringio)

        rows = list(reader)

        file_type = classify_file_type(rows)

        if file_type == "DV 360 - Case 1":
            merged_df = process_case_1(uploaded_file, rows, merged_df)
        elif file_type == "DV 360 - Case 2":
            merged_df = process_case_2(uploaded_file, rows, merged_df)
        elif file_type == "Google Ads":
            merged_df = process_google_ads_logic(uploaded_file, rows, merged_df)
        elif file_type == "Google Ads case 2":
            merged_df = process_google_ads_logic_2(uploaded_file, rows, merged_df)        
        elif file_type == "CM360":
            merged_df = process_cm360_logic(uploaded_file, rows, merged_df)
        elif file_type == "CM360 case 2":
            merged_df = process_cm360_logic_2(uploaded_file, rows, merged_df)
        elif file_type == "YouTube Reservation":
            merged_df = process_youtube_reservation_logic(uploaded_file, rows, merged_df)
        elif file_type == "YouTube Reservation case 2":
            merged_df = process_youtube_reservation_logic_2(uploaded_file, rows, merged_df)
        else:
            st.warning("Unknown file type. Skipping processing for this file.")


    # Apply the extract_code function to merged_df
    merged_df['Code'] = merged_df['Description'].apply(lambda desc: extract_code(desc))
    return merged_df
def extract_code(description):
    if pd.notnull(description):
        # Tìm tất cả các chuỗi phù hợp với mẫu '2300xxx'
        matches_2300 = re.findall('2300\d{3}', description)
        # Tìm tất cả các chuỗi phù hợp với mẫu '2400xxx'
        matches_2400 = re.findall('2400\d{3}', description)
        # Trả về chuỗi đầu tiên phù hợp hoặc None nếu không có chuỗi nào phù hợp
        if matches_2300:
            return matches_2300[0]
        elif matches_2400:
            return matches_2400[0]
        else:
            return None
    else:
        # Trả về None nếu giá trị không phải là chuỗi
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
        "Bill to", "Invoice number", "Invoice date","Due Date", "Billing ID",
        "Currency", "Invoice amount", "", "Product"
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
def process_google_ads_logic(uploaded_file, rows, merged_df):
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
        rows[3][1],
        rows[4][1],
        rows[5][1],
        rows[6][1],
        "",
        rows[8][1]
    ])

    df2 = pd.DataFrame(rows[split_index:], columns=["Account ID","Order name","Account budget","Purchase Order","Description","Quantity","Units","Amount"])
    df2.reset_index(drop=True, inplace=True)
    df2 = df2[df2['Order name'] != 'Account']
    df2['source_name'] = uploaded_file.name

    new_data_df = pd.DataFrame(new_data[1:], columns=new_data[0])
    new_data_df['source_name'] = uploaded_file.name
    new_data_df = new_data_df.dropna(subset=['Billing ID'])

    merged_df = pd.concat([merged_df, new_data_df.merge(df2, on='source_name', how='inner')], ignore_index=True)
    merged_df = merged_df.dropna(subset=['Description'])
    merged_df = merged_df.drop_duplicates()
    return merged_df
def process_google_ads_logic_2(uploaded_file, rows, merged_df):
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

    df2 = pd.DataFrame(rows[split_index:], columns=["Account ID","Order name","Account budget","Purchase Order","Description","Quantity","Units","Amount"])
    df2.reset_index(drop=True, inplace=True)
    df2 = df2[df2['Order name'] != 'Account']
    df2['source_name'] = uploaded_file.name

    new_data_df = pd.DataFrame(new_data[1:], columns=new_data[0])
    new_data_df['source_name'] = uploaded_file.name
    new_data_df = new_data_df.dropna(subset=['Billing ID'])

    merged_df = pd.concat([merged_df, new_data_df.merge(df2, on='source_name', how='inner')], ignore_index=True)
    merged_df = merged_df.dropna(subset=['Description'])
    merged_df = merged_df.drop_duplicates()
    return merged_df
def process_cm360_logic(uploaded_file, rows, merged_df):
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
        rows[3][1],
        rows[4][1],
        rows[5][1],
        rows[6][1],
        "",
        rows[8][1]
    ])

    df2 = pd.DataFrame(rows[split_index:], columns=["Account ID",	"Order name",	"Purchase Order",	"Description",	"UOM",	"Unit Price",	"Quantity",	"Amount"])
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
def process_cm360_logic_2(uploaded_file, rows, merged_df):
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

    df2 = pd.DataFrame(rows[split_index:], columns=["Account ID",	"Order name",	"Purchase Order",	"Description",	"UOM",	"Unit Price",	"Quantity",	"Amount"])
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
def process_youtube_reservation_logic(uploaded_file, rows, merged_df):
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
        rows[3][1],
        rows[4][1],
        rows[5][1],
        rows[6][1],
        "",
        rows[8][1]
    ])

    df2 = pd.DataFrame(rows[split_index:], columns=["Account ID",
    "Order name",
    "Purchase Order",
    "Description",
    "Start/End Dates",
    "Rate",
    "Quantity",
    "Quantity Billed",
    "Amount"
])
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
def process_youtube_reservation_logic_2(uploaded_file, rows, merged_df):
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

    df2 = pd.DataFrame(rows[split_index:], columns=["Account ID",
    "Order name",
    "Purchase Order",
    "Description",
    "Start/End Dates",
    "Rate",
    "Quantity",
    "Quantity Billed",
    "Amount"
])
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
        output_name = st.text_input("Enter the output file name:", "output.xlsx")

        df_result = process_file(output_name, merged_df)
        st.dataframe(df_result.drop(columns=['source_name']))
        st.success(f"File processed successfully. Download your result: [{output_name}]")
        st.markdown(get_binary_file_downloader_html(output_name), unsafe_allow_html=True)

def remove_columns_without_header(df):
    # Tìm các cột không có tiêu đề
    columns_without_header = df.columns[df.columns.str.contains('Unnamed')].tolist()
    # Loại bỏ các cột không có tiêu đề
    df = df.drop(columns=columns_without_header, axis=1)
    return df

def process_file(output_name, df):
    # Apply the extract_code function
    df['Code'] = df['Description'].apply(lambda desc: extract_code(desc))

    # Remove columns without headers
    df = remove_columns_without_header(df)

    # Save to Excel file
    try:
        df.to_excel(output_name, index=False)
    except IllegalCharacterError as e:
        st.error(f"Error writing to Excel: {e}. Some special characters may not be supported.")
    
    return df


def get_csv_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode('utf-8')).decode()
    href = f'<a href="data:text/csv;base64,{b64}" download="merged_data.csv"></a>'
    return href


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{bin_file}">Download {file_label}</a>'
    return href


if __name__ == "__main__":
    main()
