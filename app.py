import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_top_sites(keyword, apiKey):
    url = "https://google.serper.dev/search"
    data = {
        "q": keyword,
        "num": 20
    }
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': apiKey
    }
    response = requests.post(url, headers=headers, json=data)
    return [item['link'] for item in response.json().get('organic', [])][:5]

def scrape_site(url, tags):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = {}
    for tag in tags:
        data[tag] = [elem.get_text(strip=True) for elem in soup.find_all(tag)]
    return data

st.title('SEO Tag Scraper')

# Sidebar for API Key input
st.sidebar.header("Settings")
apiKey = st.sidebar.text_input("Enter your SERP API Key:", type="password")

# UI Components using columns
col1, col2 = st.columns(2)
with col1:
    keyword = st.text_input('Enter the keyword:')
with col2:
    selected_tags = st.multiselect('Select tags to scrape:', ['h1', 'h2', 'h3', 'p'])

if st.button('Scrape'):
    # Check if API key is provided
    if not apiKey:
        st.warning("Please provide the SERP API Key in the sidebar.")
        st.stop()  # Use st.stop() to halt the app execution at this point

    # Show a spinner with the message "Processing..."
    with st.spinner('Processing...'):
        # Call the SERP API
        top_sites = get_top_sites(keyword, apiKey)
        
        # Scrape the Websites
        results = {}
        for site in top_sites:
            results[site] = scrape_site(site, selected_tags)
    
    # Display the Results in Streamlit using expanders
    for site, data in results.items():
        with st.expander(site):
            for tag, texts in data.items():
                st.markdown(f"**{tag}**")
                for text in texts:
                    st.write(text)
                st.write("---")
