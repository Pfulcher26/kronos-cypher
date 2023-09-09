import scrapy
import spacy
import random
import os
from data_module.country_data import country_names
from data_module.starter_text import starter_text
from data_module.abstract_phrase_base import abstract_phrase_base

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Constants
COUNTRY_LIST = country_names
INPUT_TEXT = starter_text

class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    start_urls = ["https://en.wikipedia.org/wiki/Japan"]

    def parse(self, response):
        # Extract all text content within <a> elements
        text_content = response.xpath('//a[contains(@href, "/wiki/")]/text()').extract()
        # Combine text content into a single string
        combined_text = " ".join(text_content)

        # Process the combined text with spaCy
        doc = nlp(combined_text)

        # Extract recognized entities
        recognized_entities = [entity.text for entity in doc.ents if entity.label_ == "GPE"]
        # Filter recognized entities to keep only country names
        country_names = [entity for entity in recognized_entities if entity in COUNTRY_LIST]

        # For each recognized country, make a request to its Wikipedia page
        for country_name in country_names:
            country_url = f"https://en.wikipedia.org/wiki/{country_name.replace(' ', '_')}"
            yield scrapy.Request(url=country_url, callback=self.parse_country, cb_kwargs={'country_name': country_name})

    def parse_country(self, response, country_name):
        # Extract the title of the country's Wikipedia article
        country_title = country_name  

        # Extract the main text content of the article
        text_content = " ".join(response.css('div#mw-content-text p::text').getall())

        # Extract nouns and adjectives from the input text
        nouns, adjectives = self.extract_nouns_adjectives(text_content)

