import streamlit as st
from googlesearch import *
import pandas as pd
from tqdm import tqdm  # Import tqdm for the progress bar

# Define the Streamlit app
def main():
    st.title("URL Scraper")

    # Upload a CSV file
    uploaded_file = st.file_uploader("Upload a CSV file with keywords", type=["csv"])

    if uploaded_file is not None:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Define the number of URLs to scrape for each keyword
        num_urls_to_scrape = 3

        # Create new columns in the DataFrame to store the URLs
        for i in range(num_urls_to_scrape):
            df[f'URL {i+1}'] = ''

        # Function to scrape URLs for a given keyword
        def scrape_urls(keyword):
            try:
                # Execute the query and store search results
                results = search(keyword, tld="com", lang="en", stop=num_urls_to_scrape, pause=2)
                # Get the first 'num_urls_to_scrape' search results
                urls = list(results)
                return urls
            except Exception as e:
                st.error(f"Error scraping URLs for '{keyword}': {str(e)}")
                return []

        # Iterate over the keywords and scrape URLs with a progress bar
        progress_bar = st.progress(0)
        for index, row in tqdm(df.iterrows(), total=len(df)):
            keyword = row['Keyword']
            urls = scrape_urls(keyword)
            # Store the URLs in the respective columns
            for i in range(min(len(urls), num_urls_to_scrape)):
                df.at[index, f'URL {i+1}'] = urls[i]

            # Update the progress bar
            progress_bar.progress((index + 1) / len(df))

        # Display the DataFrame with URLs
        st.write(df)

        # Allow the user to download the updated CSV file
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False).encode(),
            file_name="output.csv",
            key="download-button"
        )

# Run the Streamlit app
if __name__ == "__main__":
    main()
