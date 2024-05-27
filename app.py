import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_top_sites(keyword, apiKey):
    logger.debug(f"Fetching top sites for keyword: {keyword}")
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
    logger.debug(f"Response Status Code: {response.status_code}")
    if response.status_code != 200:
        logger.error(f"Error fetching top sites: {response.text}")
        return []
    return [item['link'] for item in response.json().get('organic', [])][:10]

def scrape_site(url, tags):
    logger.debug(f"Scraping site: {url} for tags: {tags}")
    response = requests.get(url)
    logger.debug(f"Response Status Code: {response.status_code}")
    if response.status_code != 200:
        logger.error(f"Error scraping site: {response.text}")
        return {}
    soup = BeautifulSoup(response.content, 'html.parser')
    data = {}
    for tag in tags:
        data[tag] = [elem.get_text(strip=True) for elem in soup.find_all(tag)]
    return data

def generate_hyper_optimized_brief(consolidated_data, openai_api_key, keyword):
    logger.debug("Generating hyper-optimized brief")
    detailed_message = f"You are a seasoned SEO expert and content strategist. Your task is to analyze the following consolidated data from top-ranking websites and provide a hyper-optimized content brief focused around the keyword '{keyword}'. This brief should be actionable and clear for content writers, highlighting key points and takeaways.\n\n"
    for tag, texts in consolidated_data.items():
        detailed_message += f"{tag}: {' '.join(texts[:10])}\n"
    detailed_message += f"\nConsider the most relevant information, avoid fluff, and provide a concise yet comprehensive brief about the intent & content using the top ranking sites, focusing particularly on the keyword '{keyword}'. Generate an optimized content brief with content idea thesis, specifying whether it's a content piece, a calculator, a landing page, or other. Format the brief in Markdown."

    logger.debug("Creating OpenAI client")
    client = OpenAI(api_key=openai_api_key)
    try:
        response = client.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a seasoned SEO expert and content strategist. Your task is to analyze the following consolidated data from top-ranking websites and provide a hyper-optimized content brief & optimal structure outline with the data of the heading given. This brief should be actionable and clear for content writers, highlighting key points and takeaways.\n\n Use the keyword's intent & context."},
            {"role": "user", "content": detailed_message}
        ])
    except Exception as e:
        logger.error(f"Error generating brief with OpenAI: {e}")
        return "Error generating brief with OpenAI."

    return response.choices[0].message.content

# Streamlit UI code
st.title('SEO Tag Scraper')
st.write("""
This tool allows you to scrape SEO-related tags from the top-ranking sites for a specific keyword.
To get started, you'll need an API key from SERPer Dev & OpenAI. If you don't have one, get it [SERPer Dev](https://serper.dev) & [OpenAI](https://platform.openai.com/).
""")

st.sidebar.header("Settings")
st.sidebar.write("""
Please enter your SERPer Dev & OpenAI API key below. This key is used to fetch the top-ranking sites for your keyword and provide you with a hyper personalized content brief.
""")
serp_api_key = st.sidebar.text_input("Enter your SERP API Key:", type="password")
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

col1, col2 = st.columns(2)
with col1:
    keyword = st.text_input('Enter the keyword:')
with col2:
    selected_tags = st.multiselect('Select tags to scrape:', ['h1', 'h2', 'h3', 'p'])

if st.button('Scrape'):
    if not serp_api_key:
        st.warning("Please provide the SERP API Key in the sidebar.")
        st.stop()

    if not openai_api_key:
        st.warning("Please provide the OpenAI API Key in the sidebar.")
        st.stop()

    if not keyword:
        st.warning("Please enter a keyword.")
        st.stop()

    if not selected_tags:
        st.warning("Please select at least one tag to scrape.")
        st.stop()

    # Show a spinner with the message "Processing..."
    with st.spinner('Processing...'):
        try:
            logger.debug("Calling get_top_sites")
            top_sites = get_top_sites(keyword, serp_api_key)
            logger.debug(f"Top sites: {top_sites}")

            if not top_sites:
                st.error("Failed to fetch top sites. Check your SERP API key and try again.")
                st.stop()

            # Scrape the Websites
            results = {}
            for site in top_sites:
                logger.debug(f"Scraping site: {site}")
                results[site] = scrape_site(site, selected_tags)
                logger.debug(f"Scraped data from {site}: {results[site]}")
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            st.error("An error occurred during scraping. Please check the logs for more details.")
            st.stop()

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

    # Generate the hyper-optimized content brief
    try:
        logger.debug("Generating hyper-optimized content brief")
        brief = generate_hyper_optimized_brief(consolidated_data, openai_api_key, keyword)
        st.markdown("### Hyper-Optimized Content Brief")
        st.markdown(brief)
    except Exception as e:
        logger.error(f"Error generating brief with OpenAI: {e}")
        st.error("An error occurred while generating the content brief with OpenAI. Please check the logs for more details.")
