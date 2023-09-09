import streamlit as st
import pandas as pd
from googlesearch import search
from tqdm import tqdm

# Function to scrape URLs for a given keyword
def scrape_urls(keyword, num_urls_to_scrape):
    try:
        # Execute the query and store search results
        results = search(keyword, tld="com", lang="en", stop=num_urls_to_scrape, pause=2)
        # Get the first 'num_urls_to_scrape' search results
        urls = list(results)
        return urls
    except Exception as e:
        st.error(f"Error scraping URLs for '{keyword}': {str(e)}")
        return []

# Streamlit app
def main():
    st.title("Keyword URL Scraper")
    
    # Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        num_urls_to_scrape = st.slider("Number of URLs to Scrape per Keyword", min_value=1, max_value=10, value=3)
        
        # Create new columns in the DataFrame to store the URLs
        for i in range(num_urls_to_scrape):
            df[f'URL {i+1}'] = ''
        
        # Iterate over the keywords and scrape URLs with a progress bar
        with st.spinner("Scraping URLs..."):
            for index, row in tqdm(df.iterrows(), total=len(df)):
                keyword = row['Keyword']
                urls = scrape_urls(keyword, num_urls_to_scrape)
                # Store the URLs in the respective columns
                for i in range(min(len(urls), num_urls_to_scrape)):
                    df.at[index, f'URL {i+1}'] = urls[i]

            st.success(f"URLs scraped successfully!")
        
        # Display the DataFrame with scraped URLs
        st.write(df)
        
        # Offer to download the updated DataFrame as a CSV file
        if st.button("Download CSV"):
            st.write(df.to_csv(index=False))

if __name__ == "__main__":
    main()
