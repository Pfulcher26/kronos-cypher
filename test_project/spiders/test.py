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
