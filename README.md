# README for CSV Merger and Converter Application

## Overview
This application, built with **Streamlit**, provides a user-friendly interface for processing and merging multiple CSV files containing invoice and billing data. The tool automatically classifies the file type based on its content and applies the appropriate processing logic to extract, transform, and unify the data into a consolidated format.

## Features
1. **Multiple File Uploads**: Supports uploading multiple CSV files simultaneously.
2. **File Type Classification**: Identifies file types using predefined rules based on file content.
3. **Data Transformation**:
   - Extracts key billing and invoice data.
   - Processes data according to specific formats (e.g., DV 360, Google Ads, CM360, YouTube Reservation).
   - Removes duplicates and columns without headers.
4. **Custom Output**: Allows users to define the output file name.
5. **Downloadable Result**: Provides a processed CSV file for download.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <project-folder>
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Open the application in your browser using the Streamlit URL (e.g., `http://localhost:8501`).
2. Upload one or more CSV files using the file uploader.
3. Enter a name for the output file.
4. View the processed data in the preview table.
5. Download the resulting file by clicking the provided download link.

## File Classification Logic
The application determines the file type based on content found in specific rows:
- **DV360 - Case 1/2**
- **Google Ads - Case 1/2**
- **CM360 - Case 1/2**
- **YouTube Reservation - Case 1/2**
- **Unknown**: Files that do not match any predefined cases.

## Key Functions
- **`classify_file_type(rows)`**: Identifies the type of input file based on its rows.
- **`split_and_convert_data(input_files)`**: Iterates over uploaded files and applies the correct processing logic.
- **`process_case_X`**: Handles data transformation for specific file types.
- **`extract_code(description)`**: Extracts special codes (`2300xxx` or `2400xxx`) from descriptions using regular expressions.

## Output Format
The processed output contains the following columns (depending on the file type):
- `Bill to`
- `Invoice number`
- `Invoice date`
- `Due Date`
- `Billing ID`
- `Currency`
- `Invoice amount`
- `Product`
- `Order name`
- `Purchase Order`
- `Description`
- Additional columns specific to the file type

## Notes
- The application requires input files to be in CSV format and expects specific header structures for processing.
- Unknown file types will be skipped with a warning message.

## Troubleshooting
- **File type not recognized**: Ensure that the input file conforms to one of the expected formats.
- **Incorrect data in output**: Verify the structure and content of the input files.

## Future Enhancements
- Add support for more file types.
- Include advanced error handling and logging.
- Allow file preview before processing. 

---

For further assistance, please contact the repository maintainer.
