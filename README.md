
# Data Forensics Project

This is a drug market analysis project based on the data crawled and scraped from dark web drug marketplaces. It has 2 main folders, one is the python app for the interactive dashboard and other one is the collection of scrapers and crawlers we have used. All the scrapers and crawlers are implemented by ourselves.




## ForensicsDarkWeb folder
This folder contains ourr crawlers and scrapers with the raw data we got from the marketplaces (html files) with those data scraped into csv and json file formats.

## ForensicsDashboard folder
This folder contains the dash app and its helper scripts. Within this folder you can find app folder which contains the dash app and the data.py file inside that folder is used for data preprocessing. Data folder contains json and csv files of data. Data Fixing contains 4 files. Classifier.py classifies the drug types usin OpenAI LLM api, json_combiner.py combines all json files into one, marketplace_adder.py adds the marketplace value to each drug object based on their file name, price_fixer.py standardize the price values. 




## Authors

- [@GeorgeAntono](https://www.github.com/GeorgeAntono)
- [@Canonal7](https://www.github.com/Canonal7)


