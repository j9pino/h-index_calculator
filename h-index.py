import streamlit as st
import pandas as pd
import numpy as np

def calculate_h_index(citations):
    citations = sorted(citations, reverse=True)
    h_index = 0
    for i, c in enumerate(citations):
        if c >= i + 1:
            h_index = i + 1
        else:
            break
    return h_index

st.title('H-index Calculator')

uploaded_file = st.file_uploader("Upload a CSV file with only the following columns: Title, Year, and Citations. Please remember to delete any file details before the first row of publication information. This program will calculate the overall h-index from a list of publications and the h-index by year. It cannot determine h-index by author at this time.", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Handle different column name variations
    column_mappings = {
        'Title': 'title',
        'Year': 'year',
        'Citations': 'citations'
    }
    
    df.columns = [column_mappings.get(col, col) for col in df.columns]

    # Ensure required columns are present
    if 'year' in df.columns and 'citations' in df.columns:
        # Drop rows with any missing values
        df.dropna(subset=['year', 'citations'], inplace=True)

        st.write("Data Preview")
        st.dataframe(df.head())

        # Calculate overall h-index
        overall_h_index = calculate_h_index(df['citations'].tolist())
        st.write(f"Overall h-index: {overall_h_index}")

        # Calculate h-index by year
        years = df['year'].unique()
        h_index_by_year = {}
        for year in years:
            year_citations = df[df['year'] == year]['citations'].tolist()
            h_index_by_year[year] = calculate_h_index(year_citations)

        st.write("h-index by Year:")
        h_index_df = pd.DataFrame(list(h_index_by_year.items()), columns=['Year', 'h-index'])
        h_index_df = h_index_df.sort_values(by='Year', ascending=False)  # Sort years in descending order
        st.dataframe(h_index_df)

        # Option to download the results
        csv = h_index_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download h-index by Year as CSV",
            data=csv,
            file_name='h_index_by_year.csv',
            mime='text/csv',
        )
    else:
        st.error("The CSV file must contain 'year' and 'citations' columns.")
