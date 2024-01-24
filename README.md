# web-scrapper-python
## Description

What it does?
Scrapes the data inside pdfs present at provided stock exchange news url matching given keyword,stores it to pinecone vector store,returns data which is required to insert in excel file.

This is simple python script (using python3) which scrapes and gets data from pdf using OpenAI  

## Installation

```bash
$ add openAI api key in file  
```

```bash
$ pip install 
```


## Running the app

```bash
# development
$ python3 scrap.py


when python script is successfully  

EXPECTED RESPONSE in data.json file
[
{
"SrNo": 1,
"StockExchange": "HKEX",
"DateOfResignation": "24-Jan-2024",
"CompanyTicker": "834 HK",
"CompanyName": "China Kangda Food Company Limited",
"ResigningExecutiveDirector": ["Mr. Luo Zhenwu", "Mr. Li Wei"],
"ReasonForResignation": "Focus on their respective other business pursuits and commitments",
"NewAppointment": "In process of identifying a suitable candidate"
},
{
"SrNo": 2,
"StockExchange": "HKEX",
"DateOfResignation": "23-Jan-2024",
"CompanyTicker": "Not Provided",
"CompanyName": "Huscoke Holdings Limited",
"ResigningNonExecutiveDirector": "Mr. Tang Ching Fai",
"ReasonForResignation": "Desire to devote more time to his personal engagements",
"NewAppointment": "Not Provided"
},
{
"SrNo": 3,
"StockExchange": "HKEX",
"DateOfResignation": "Not Provided",
"CompanyTicker": "02611 HK",
"CompanyName": "Guotai Junan Securities Co., Ltd.",
"ResigningViceChairmanAndPresident": "Mr. WANG Song",
"ReasonForResignation": "Reached the retirement age",
"NewAppointment": "Not Provided"
}
]

