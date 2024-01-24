from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import fitz
import requests
from openai import OpenAI
import re
import json
import os


# add you openai key 
client = OpenAI(api_key='')



def scrape_website(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url , wait_until="networkidle")
        # page.wait_for_load_state("load")
        selectors_to_wait = ['.table', '.container', '.table-scroller' , '#hkex_news_megamenu' ]
        for selector in selectors_to_wait:
            page.wait_for_selector(selector)


        content = page.content()
        context.close()
        browser.close()

    return content


# scrape website using beautifulSoup lib
def parse_html(html , base_url):

    soup = BeautifulSoup(html, 'html.parser')
    # Add your scraping logic using BeautifulSoup here
    # For example, if you want to extract all the links on the page:
    # links = soup.find_all('a')
    # pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))
    # pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))
    # pdf_links = soup.select('.table-scroller-container a[href$=".pdf"]')
    pdf_links = soup.select('body a[href$=".pdf"]')

    result_array = []

    for link in pdf_links:
        full_path = urljoin(base_url, link.get('href'))
        result_array.append({
            'link': full_path,
            'text': link.text.strip()  # Assuming you want the text within the <a> tag
        })
    # print(result_array)
    # print(len(result_array))
    return result_array
    # for link in pdf_links:
    #     print(link.get('href'))


# get response from openai 
def get_openAiRes(filterPdfs):
    responseArray = []
    print("processing total pdfs : " + str(len(filterPdfs)))
    i=0
    for pdf_url in filterPdfs:
        raw_text = read_pdf_text_from_url(pdf_url)
        # print(raw_text)
        

        completion = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. strictly give answers based on given content"},
                {"role" : "assistant" ,  "content" : "based on user query give response if not found just say DATA NOT FOUND"  } ,
                {"role": "user", "content": """ Generate a json response containing information about resignation details about auditor and new appointments from [stock market news data : %s ]. Include all the properties as shown in example.
                [{
                    "SrNo.":1,
                    "StockExchange":"HKEX",
                    "DateOfResignation":"03-Dec-2021",
                    "CompanyTicker":"8491 HK",
                    "CompanyName":"Cool Link (Holdings)",
                    "ResigningAuditor":"Grant Thornton HK Ltd ",
                    "ReasonForResignation":"Could not reach a consensus on the audit fee.",
                    "NewAuditorAppointmentDate":"03-Dec-2021",
                    "NewAuditorName":"UniTax Prism (HK) CPA Ltd "
                },...,...] """ % (raw_text) }]
        )
        
       
        openaiRes = completion.choices[0].message.content
        json_array_pattern = re.compile(r'\[.*?\]', re.DOTALL)
        json_array_match = json_array_pattern.search(openaiRes)
        i+=1;
        print("""%s - pdf processed"""%(i))
        if json_array_match:
            json_array = json_array_match.group()
            json_object = json.loads(json_array)
            responseArray.append(json_object[0])
        else:
            # print("No JSON array found in the given text.")
            print("")


    return responseArray


# extract text from pdf's
# def read_pdf_text(file_path):
    doc = fitz.open(file_path)
    text = ""
    
    for page_number in range(doc.page_count):
        page = doc[page_number]
        text += page.get_text()
    
    doc.close()
    return text


# extract text from pdf's
def read_pdf_text_from_url(pdf_url):
    response = requests.get(pdf_url)
    with open("temp.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)
    
    doc = fitz.open("temp.pdf")
    text = ""
    
    for page_number in range(doc.page_count):
        page = doc[page_number]
        text += page.get_text()
    
    doc.close()
    return text


if __name__ == "__main__":
    target_url = "https://www1.hkexnews.hk/listedco/listconews/index/lci.html" 

    # scrape all html
    html_content = scrape_website(target_url)
    
    # Get All PDF's Links 
    result = parse_html(html_content , target_url)

    
    # filter by keyword
    keyword = "Resignation"
    filtered_data = [obj for obj in result if keyword.lower() in obj['text'].lower()]

    print("Website Scraped Successfully !")
    # Send pdf List - process one by one - get response from open ai - store to object - get that object 
    links = [item['link'] for item in filtered_data]
    # print(links)
    print("Starting to process pdfs ...")
    OpenAiRes = get_openAiRes(links)
    print("Response from openAI ")
    with open('./data.json', 'w') as json_file:
        json.dump(OpenAiRes, json_file, indent=4)

    
    print(f"Data saved to JSON file  !")

