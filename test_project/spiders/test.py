import scrapy

class AuthorsSpider(scrapy.Spider):
    name = 'first_spider'
    start_urls = ['https://en.wikipedia.org/wiki/Johannesburg']

    def parse(self, response):
        # Use the class selector to target the main content container
        page_container = response.css('main#content') 
        # Check if the element was found
        if page_container:
            # Extract the text content from paragraphs within the container
            paragraphs = page_container.css('p::text').getall()
            # Join the paragraphs into a single string
            text_content = ' '.join(paragraphs)
            
            # You can save the text content to a file if needed
            with open('output.txt', 'w', encoding='utf-8') as file:
                file.write(text_content)
            
            # Or you can store it in a variable for further processing
            # self.text_content = text_content
        else:
            self.log("Element with class 'mw-page-container' not found on the page.")
