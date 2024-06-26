# SERP Content Brief Generator Documentation

## Overview
The SERP Content Brief Generator is a powerful tool designed to help SEO professionals and content strategists scrape SEO-related tags from top-ranking sites for a specific keyword and generate a hyper-optimized content brief using OpenAI's GPT-4o. This brief can be used to create high-quality, SEO-friendly content that aligns with the top-performing content on the web.

## Features
- Fetch top-ranking sites for a specific keyword using SERPer Dev API.
- Scrape specified HTML tags (e.g., h1, h2, h3, p) from these sites.
- Consolidate the scraped data.
- Generate a hyper-optimized content brief using OpenAI's GPT-4o model.
- User-friendly interface built with Streamlit.

## Prerequisites
- Python 3.7 or higher
- API key from SERPer Dev
- API key from OpenAI
- Required Python libraries listed in `requirements.txt`

## Installation
1. Clone the repository or download the script.
2. Ensure you have Python installed on your machine.
3. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application
To start the Streamlit application, navigate to the directory containing your script and run:
```bash
streamlit run app.py
```

### User Interface
1. **Settings (Sidebar)**:
   - **Enter your SERPer Dev API Key**: This key is used to fetch the top-ranking sites for your keyword.
   - **Enter your OpenAI API Key**: This key is used to generate the content brief.

2. **Main Interface**:
   - **Enter the keyword**: Type in the keyword for which you want to scrape and analyze top-ranking sites.
   - **Select tags to scrape**: Choose the HTML tags you want to scrape from the top-ranking sites (e.g., h1, h2, h3, p).

3. **Scrape Button**:
   - Click the "Scrape" button to initiate the scraping process. The application will fetch the top sites, scrape the selected tags, and display the results.

4. **Results**:
   - Scraped data from each site will be displayed under expandable sections. The data is consolidated and used to generate a hyper-optimized content brief.

5. **Hyper-Optimized Content Brief**:
   - The content brief generated by OpenAI will be displayed, providing actionable insights and a content structure outline based on the keyword and scraped data.

## Example Workflow
1. Open the application using Streamlit.
2. Enter your SERPer Dev and OpenAI API keys in the sidebar.
3. Type in the keyword you are targeting, such as "best running shoes 2024".
4. Select the HTML tags you are interested in scraping, such as `h1`, `h2`, `h3`, and `p`.
5. Click "Scrape" to begin the process.
6. Review the scraped data displayed in expandable sections.
7. View and use the hyper-optimized content brief generated for your keyword.

## Error Handling
- If there is an error fetching the top sites or scraping the data, appropriate error messages will be displayed.
- Ensure that the provided API keys are correct and have the necessary permissions.
- Check the console or logs for detailed error messages if something goes wrong.

## Additional Notes
- The tool relies on the SERPer Dev API for fetching top-ranking sites and the OpenAI API for generating content briefs. Make sure you have valid API keys and sufficient quota for both services.
- Customize the scraping and brief generation logic as needed to fit your specific use case or requirements.

## License
This project is licensed under the MIT License.

For further questions or support, please contact the project maintainers or refer to the official documentation of the libraries and APIs used.

---

This documentation provides a comprehensive guide to installing, configuring, and using the SERP Content Brief Generator. It includes all necessary details to help users understand and make the most of the tool.
