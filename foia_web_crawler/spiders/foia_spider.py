import os
import scrapy

class FoiaSpider(scrapy.Spider):
    name = "foia_spider"
    
    start_urls = [
        "https://www.tsa.gov/foia/readingroom",
        "https://www.ice.gov/foia/library"
    ]
    
    custom_settings = {
        'DEPTH_LIMIT': 3  # Limit the depth to avoid getting stuck in a loop
    }
    
    visited_urls = set()

    def parse(self, response):
        # Create base directory for storing PDFs
        base_dir = 'C:/Users/scoll/OneDrive/Documents/foia'
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        self.logger.info(f"Base directory created: {base_dir}")
        
        # Determine the sub-directory based on the source URL
        if "tsa.gov" in response.url:
            sub_dir = "TSA"
        elif "ice.gov" in response.url:
            sub_dir = "ICE"
        else:
            sub_dir = "Misc"
        
        save_dir = os.path.join(base_dir, sub_dir)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # Find all PDF links on the current page
        pdf_links = response.css('a::attr(href)').re(r'.*\.pdf$')
        self.logger.info(f"Found {len(pdf_links)} PDF links on {response.url}")
        for pdf_link in pdf_links:
            pdf_url = response.urljoin(pdf_link)
            self.logger.info(f"Found PDF link: {pdf_url}")
            yield scrapy.Request(pdf_url, callback=self.save_pdf, meta={'save_dir': save_dir})

        # Find all links on the current page and follow them if they haven't been visited
        additional_links = response.css('a::attr(href)').re(r'/.*')
        for link in additional_links:
            next_page = response.urljoin(link)
            if next_page not in self.visited_urls:
                self.visited_urls.add(next_page)
                self.logger.info(f"Found additional link: {next_page}")
                yield scrapy.Request(next_page, callback=self.parse)
    
    def save_pdf(self, response):
        save_dir = response.meta['save_dir']
        file_name = response.url.split("/")[-1]
        file_path = os.path.join(save_dir, file_name)
        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.logger.info(f"Downloaded: {file_path}")

# Save this script in the spiders directory and run with `scrapy crawl foia_spider --loglevel=DEBUG`
