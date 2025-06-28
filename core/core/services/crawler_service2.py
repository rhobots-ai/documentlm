import json
import shutil
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests

# --- Installation ---
# Before running, please install the required libraries:
# pip install scrapy requests
# Note: Scrapy may have other dependencies depending on your OS.

import os
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'scrapy.settings.default')
from twisted.internet import asyncioreactor
# Ensure asyncio reactor is installed if running in a non-standard environment
if 'twisted.internet.reactor' in sys.modules:
    del sys.modules['twisted.internet.reactor']
asyncioreactor.install()


import scrapy
from scrapy.spiders import SitemapSpider
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field



class DocumentItem(Item):
    """Represents a single document found."""
    doc_url = Field()
    doc_text = Field()


class PageItem(Item):
    """Represents a page and the documents found on it."""
    page_url = Field()
    page_title = Field()
    sections = Field() # This will be a dictionary of lists of DocumentItems


# --- Scrapy Pipeline Definition ---
class JsonStructurePipeline:
    """
    This pipeline collects all items from the spider and writes them
    to a single JSON file upon completion.
    """
    def __init__(self):
        self.all_pages_data = []

    def process_item(self, item, spider):
        # The ItemAdapter makes it easy to convert Scrapy Items to dicts
        self.all_pages_data.append(dict(item))
        return item

    def close_spider(self, spider):
        # This method is called when the spider finishes.
        # We get the output filename from the spider's attributes.
        output_filename = getattr(spider, 'output_filename', 'discovered_documents.json')
        print(f"--- Saving hierarchical results to {output_filename} ---")
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(self.all_pages_data, f, indent=4, ensure_ascii=False)
        print(f"Results saved successfully.\n")


# --- Scrapy Spider Definition ---
# This spider contains the core logic for crawling and extracting data.
class HierarchicalScrapySpider(SitemapSpider):
    """
    A Scrapy spider that crawls a site using its sitemap.xml, finds document
    links, and organizes them into a hierarchical structure.
    """
    name = 'hierarchical_sitemap_spider'

    # Define the file extensions to look for
    target_file_extensions = {
        '.pdf', '.mp3', '.wav', '.mp4', '.mov', '.avi',
        '.xls', '.xlsx', '.doc', '.docx', '.ppt', '.pptx'
    }

    def __init__(self, *args, **kwargs):
        # We pass the sitemap_url dynamically when we start the crawl
        self.sitemap_urls = [kwargs.get('sitemap_url')]
        self.output_filename = kwargs.get('output_filename')
        super(HierarchicalScrapySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        """
        This method is called for each URL found in the sitemap. It extracts
        document links and finds their associated section headings.
        """
        print(f"  -> Parsing: {response.url}")

        page_item = PageItem()
        page_item['page_url'] = response.url
        page_item['page_title'] = response.css('title::text').get()
        page_item['sections'] = {}

        # Use CSS selectors to find all links pointing to target file types
        selectors = [f'a[href$="{ext}"]' for ext in self.target_file_extensions]
        for link_selector in response.css(", ".join(selectors)):
            doc_item = DocumentItem()
            doc_item['doc_url'] = response.urljoin(link_selector.css('::attr(href)').get())
            doc_item['doc_text'] = "".join(link_selector.css('::text').getall()).strip() or "No Text Found"

            # Use XPath to find the nearest preceding heading (h1-h4)
            heading = link_selector.xpath('preceding::*[self::h1 or self::h2 or self::h3 or self::h4][1]/text()').get()
            heading_text = heading.strip() if heading else "General"

            if heading_text not in page_item['sections']:
                page_item['sections'][heading_text] = []

            page_item['sections'][heading_text].append(dict(doc_item))

        # If any documents were found on this page, yield the entire PageItem
        if page_item['sections']:
            yield page_item


# --- Main Application Class ---
# This class orchestrates the entire workflow.

class CrawlerApp:
    def __init__(self, start_url: str, download_dir='temp_downloads'):
        if not start_url.startswith(('http://', 'https://')):
            raise ValueError("Invalid start_url. It must be a valid HTTP/HTTPS URL.")

        self.start_url = start_url
        self.base_domain = urlparse(start_url).netloc
        self.sitemap_url = urljoin(start_url, '/sitemap.xml')
        self.download_dir = Path(download_dir)
        self.results_file = "discovered_documents.json"

        self.download_dir.mkdir(exist_ok=True)
        print(f"Application initialized for domain: {self.base_domain}")
        print(f"Using sitemap: {self.sitemap_url}")
        print(f"Temporary files will be downloaded to: {self.download_dir}\n")

    def _get_normalized_filename(self, url: str) -> str:
        path = urlparse(url).path
        return Path(path).name

    def run_crawl(self):
        """
        Configures and runs the Scrapy SitemapSpider using CrawlerProcess.
        This will generate the JSON output file via the pipeline.
        """
        print(f"--- Step 1: Starting Scrapy Sitemap crawl ---")

        # Settings for the Scrapy process
        process_settings = {
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'ROBOTSTXT_OBEY': True,
            'LOG_LEVEL': 'INFO', # Use 'DEBUG' for more verbose output
            'ITEM_PIPELINES': {__name__ + '.JsonStructurePipeline': 300},
        }

        process = CrawlerProcess(settings=process_settings)
        process.crawl(
            HierarchicalScrapySpider,
            sitemap_url=self.sitemap_url,
            output_filename=self.results_file
        )
        process.start() # The script will block here until the crawl is finished

    def load_crawl_results(self) -> list[dict]:
        """Loads the results from the JSON file created by the crawl."""
        print(f"--- Step 2: Loading results from {self.results_file} ---")
        try:
            with open(self.results_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Successfully loaded data for {len(data)} pages.\n")
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Could not find or parse {self.results_file}. Returning empty list.\n")
            return []

    def get_files_from_external_source(self) -> list[str]:
        """Placeholder function to get a list of already processed file URLs."""
        print("--- Step 3: Getting list of previously processed files from external source ---")
        mock_files = ['https://rbidocs.rbi.org.in/rdocs/content/pdfs/Utkarsh30122022.pdf']
        print(f"Found {len(mock_files)} pre-existing files from external source.\n")
        return mock_files

    def process_files_via_api(self, file_urls: list[str]):
        """Downloads and sends new files to a simulated third-party API."""
        print(f"--- Step 5: Processing {len(file_urls)} newly added files ---")
        if not file_urls:
            print("No new files to process.\n")
            return

        for file_url in file_urls:
            print(f"  -> Processing: {file_url}")
            try:
                response = requests.get(file_url, stream=True, timeout=30)
                response.raise_for_status()
                filename = self._get_normalized_filename(file_url) or "downloaded_file"
                temp_file_path = self.download_dir / filename

                with open(temp_file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"     - Downloaded to: {temp_file_path}")
                print(f"     - Source for implementation: Send '{temp_file_path}' to a 3rd party API.")

            except Exception as e:
                print(f"     - Failed to process {file_url}: {e}")
        print("Finished processing files.\n")

    def finalize_run(self, processed_files: list[str]):
        """Prints a final summary and cleans up downloaded files."""
        print("--- Step 6: Finalizing Run ---")
        if processed_files:
            print("\nThe following new files were processed in this run:")
            for url in processed_files:
                print(f"  - {url}")
        else:
            print("\nNo new files were found to process in this run.")

        print("\nCleaning up temporary download directory...")
        try:
            shutil.rmtree(self.download_dir)
            print(f"Successfully removed {self.download_dir}")
        except Exception as e:
            print(f"Error cleaning up directory '{self.download_dir}': {e}")


# --- Main Execution Logic ---
if __name__ == '__main__':
    TARGET_URL = "https://rbi.org.in/home.aspx"

    app = CrawlerApp(start_url=TARGET_URL)

    # 1. Initialize and run the Scrapy crawl. This creates the results JSON file.
    app.run_crawl()

    # 2. Load the hierarchical data from the file created by the crawl.
    hierarchical_data = app.load_crawl_results()

    # 3. Get the list of files that are already known from another source.
    files_already_in_system = app.get_files_from_external_source()
    filenames_already_in_system = {app._get_normalized_filename(url) for url in files_already_in_system}

    # 4. Flatten the hierarchical data to get a list of all discovered URLs for comparison.
    all_files_on_site = []
    for page in hierarchical_data:
        for docs in page.get('sections', {}).values():
            for doc in docs:
                all_files_on_site.append(doc['doc_url'])

    newly_added_files = []
    for url in all_files_on_site:
        if app._get_normalized_filename(url) not in filenames_already_in_system:
            newly_added_files.append(url)

    print(f"--- Step 4: Comparing discovered files with existing files ---")
    print(f"Found {len(newly_added_files)} new files to be processed.\n")

    # 5. Process only the newly added files via the API.
    app.process_files_via_api(newly_added_files)

    # 6. Finalize the run and clean up.
    app.finalize_run(newly_added_files)
