import streamlit as st
import pandas as pd
import io

# Streamlit app title
st.title("Roll Number Data Filter")

# Input for roll number
roll_no = st.text_input("Enter your roll number", "")

# URL of the CSV file on GitHub (replace with your actual raw GitHub URL)
csv_url = "Students Mid Sem Exam Time Table Autumn 2025(Room allocation).csv" 

if roll_no:
    try:
    	# Read the CSV file from GitHub
        df = pd.read_csv(csv_url)

        # Filter rows where the roll number is in 'rollnolist'
        filtered_df = df[df['rollnolist'].apply(lambda x: roll_no in str(x).split(','))]

        # Sort by 'date' column
        filtered_df = filtered_df.sort_values(by='date')

        if filtered_df.empty:
            st.warning(f"No data found for roll number {roll_no}.")
        else:
            # Drop the 'rollnolist' column
            filtered_df = filtered_df.drop(columns=['rollnolist'])

            # Convert DataFrame to Excel
            output = io.BytesIO()
            filtered_df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            # Provide download button
            st.download_button(
                label="Download Excel File",
                data=output,
                file_name=f"seat_plan_{roll_no}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Display the filtered data
            st.write("Seat Plan:")
            st.dataframe(filtered_df)

    except Exception as e:
        st.error(f"Error loading or processing the CSV file: {str(e)}")
else:
    st.info("Please enter a roll number to filter the data.")
