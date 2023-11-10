import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

def get_top_sites(keyword, apiKey):
    url = "https://google.serper.dev/search"
    data = {
        "q": keyword,
        "num": 10,
        "gl": "us"
    }
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': apiKey
    }
    response = requests.post(url, headers=headers, json=data)
    return [item['link'] for item in response.json().get('organic', [])][:10]

def scrape_site(url, tags):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = {}
    for tag in tags:
        data[tag] = [elem.get_text(strip=True) for elem in soup.find_all(tag)]
    return data

def generate_hyper_optimized_brief(consolidated_data, openai_api_key):
    # Introductory context
    # detailed_message = "You are a seasoned SEO expert and content strategist. Your task is to analyze the following consolidated data from top-ranking websites and provide a hyper-optimized content brief and thesis. This brief should be actionable and clear for content writers, highlighting key points and takeaways.\n\n"

    # Add the scraped data
    for tag, texts in consolidated_data.items():
        detailed_message = f"{tag}: {' '.join(texts[:10])}\n"  # Using first 3 items for brevity

    # Additional instructions for clarity and conciseness
    detailed_message += "\nConsider the most relevant information, avoid fluff, and provide a concise yet comprehensive brief about the intent & content using the top ranking sites. Generate a optimised content brief with content idea thesis. give what we need to build is it a content piece or a calculator or a Landing page or other things. in Markdown"

    openai.api_key = openai_api_key
    completion = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a seasoned SEO expert and content strategist. Your task is to analyze the following consolidated data from top-ranking websites and provide a hyper-optimized content brief & optimal structure outline with the data of the heading given. This brief should be actionable and clear for content writers, highlighting key points and takeaways.\n\n"},
            {"role": "user", "content": detailed_message}
        ]
    )

    return completion.choices[0].message["content"]

st.title('SEO Tag Scraper')
st.write("""
This tool allows you to scrape SEO-related tags from the top-ranking sites for a specific keyword.
To get started, you'll need an API key from SERPer Dev & OpenAI Api (it uses gpt-3.5-turbo-16k) If you don't have one, get it [SERPer Dev](https://serper.dev) & [OpenAI](https://platform.openai.com/).
""")

# Sidebar for API Key input
st.sidebar.header("Settings")
st.sidebar.write("""
Please enter your SERPer Dev & OpenAI API key below. This key is used to fetch the top-ranking sites for your keyword, & using it give you a hyper personalised content brief
""")
serp_api_key = st.sidebar.text_input("Enter your SERP API Key:", type="password")
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

# UI Components using columns
col1, col2 = st.columns(2)
with col1:
    keyword = st.text_input('Enter the keyword:')
with col2:
    selected_tags = st.multiselect('Select tags to scrape:', ['h1', 'h2', 'h3', 'p'])

if st.button('Scrape'):
    # Check if SERP API key is provided
    if not serp_api_key:
        st.warning("Please provide the SERP API Key in the sidebar.")
        st.stop()

    # Show a spinner with the message "Processing..."
    with st.spinner('Processing...'):
        # Call the SERP API
        top_sites = get_top_sites(keyword, serp_api_key)
        
        # Scrape the Websites
        results = {}
        for site in top_sites:
            results[site] = scrape_site(site, selected_tags)

    # Display the Results in Streamlit using expanders
    consolidated_data = {}
    for site, data in results.items():
        with st.expander(f"Scraped Data from {site}"):
            for tag, texts in data.items():
                st.markdown(f"**{tag}**")
                for text in texts:
                    st.write(text)
                # Consolidate data for hyper-optimized brief
                if tag not in consolidated_data:
                    consolidated_data[tag] = []
                consolidated_data[tag].extend(texts)

    # Generate and display hyper-optimized content brief and thesis, only if OpenAI API key is provided
    if openai_api_key:
        with st.expander("Hyper-Optimized Content Brief & Thesis"):
            hyper_brief = generate_hyper_optimized_brief(consolidated_data, openai_api_key)
            st.write(hyper_brief)
    else:
        st.write("OpenAI API key not provided. Skipping hyper-optimized content brief generation.")
