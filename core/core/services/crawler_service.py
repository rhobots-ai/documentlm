import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
import shutil

from playwright.sync_api import sync_playwright


# --- Installation ---
# Before running, please install the required libraries:
# pip install playwright requests
# And install the browser binaries for Playwright:
# python -m playwright install


class UrlCrawler:
	"""
	A modular service to crawl a website, identify new files based on filename,
	and process them through a simulated external API.
	"""
	
	def __init__(self, start_url: str, download_dir='temp_downloads'):
		"""
		Initializes the service.
		"""
		if not start_url.startswith(('http://', 'https://')):
			raise ValueError("Invalid start_url. It must be a valid HTTP/HTTPS URL.")
		
		self.start_url = start_url
		self.base_domain = urlparse(start_url).netloc
		self.download_dir = Path(download_dir)
		self.target_file_extensions = {'.pdf', '.mp3', '.wav', '.mp4', '.mov', '.avi', '.xls', '.xlsx', '.doc', '.docx', '.ppt', '.pptx'}
		
		self.download_dir.mkdir(exist_ok=True)
		print(f"Service initialized for URL: {self.start_url}")
		print(f"Temporary files will be downloaded to: {self.download_dir}")
	
	def _get_normalized_filename(self, url: str) -> str:
		"""
		Best practice: Extracts a clean filename from a URL by parsing its path
		and ignoring any query parameters.
		"""
		path = urlparse(url).path
		return Path(path).name
	
	def process_initial_url_with_api(self):
		"""
		1. Passes the initial URL to a third-party service that fetches and processes its content.
		"""
		print(f"--- Step 1: Passing URL to Kotaemon Function for initial url processing ---")
		print(f"Source for implementation: Call Kotaemon Function to process content from {self.start_url}\n")
	
	def get_files_from_external_source(self) -> list[str]:
		"""
		Placeholder function to get a list of already processed file URLs
		from another service or function.
		"""
		print("--- Step 2: Getting list of previously processed files from external source ---")
		
		# =================================================================
		print("Source for implementation: Call an external service to get a list of existing file URLs.")
		mock_files = [
			'https://rbidocs.rbi.org.in/rdocs/content/pdfs/Utkarsh30122022.pdf'
		]
		print(f"Found {len(mock_files)} pre-existing files from external source.\n")
		return mock_files
	
	def crawl_and_discover_files(self, max_pages: int = 50) -> list[str]:
		"""
		Crawls the website to discover all URLs pointing to files, ensuring
		that each unique filename is discovered only once per run.
		"""
		print(f"--- Step 3: Crawling {self.start_url} to discover all downloadable files ---")
		urls_to_crawl = {self.start_url}
		crawled_urls = set()
		found_file_urls = []
		files_found_this_session = set()
		
		with sync_playwright() as p:
			browser = p.chromium.launch(headless=True)
			page = browser.new_page()
			while urls_to_crawl and len(crawled_urls) < max_pages:
				current_url = urls_to_crawl.pop()
				if not current_url or current_url in crawled_urls:
					continue
				crawled_urls.add(current_url)
				try:
					page.goto(current_url, wait_until="domcontentloaded", timeout=20000)
					links = page.eval_on_selector_all('a', 'elements => elements.map(e => e.href)')
					for link in links:
						full_url = urljoin(current_url, link)
						parsed_link = urlparse(full_url)
						if parsed_link.scheme in ['http', 'https']:
							file_extension = Path(parsed_link.path).suffix.lower()
							if file_extension in self.target_file_extensions:
								normalized_name = self._get_normalized_filename(full_url)
								if normalized_name not in files_found_this_session:
									files_found_this_session.add(normalized_name)
									found_file_urls.append(full_url)
							elif parsed_link.netloc == self.base_domain and urljoin(full_url, parsed_link.path) not in crawled_urls:
								urls_to_crawl.add(urljoin(full_url, parsed_link.path))
				except Exception as e:
					print(f"  -> Could not crawl {current_url}: {e}")
			browser.close()
		print(f"Crawl complete. Discovered {len(found_file_urls)} unique files on the site.\n")
		return sorted(found_file_urls)
	
	def process_files_via_api(self, file_urls: list[str]):
		"""
		Processes a list of unique files by downloading them and sending them to a third-party API.
		"""
		print(f"--- Step 5: Processing {len(file_urls)} newly added files ---")
		if not file_urls:
			print("No new files to process.\n")
			return
		
		for file_url in file_urls:
			print(f"  -> Processing: {file_url}")
			temp_file_path = None
			try:
				# Download the file locally
				response = requests.get(file_url, stream=True, timeout=30)
				response.raise_for_status()
				filename = self._get_normalized_filename(file_url) or "downloaded_file"
				temp_file_path = self.download_dir / filename
				
				with open(temp_file_path, 'wb') as f:
					for chunk in response.iter_content(chunk_size=8192):
						f.write(chunk)
				
				# --- Implementation Required ---
				# Pass the downloaded file to a third-party API as form-data
				print(f"     - Downloaded to: {temp_file_path}")
				print(f"     - Source for implementation: Send '{temp_file_path}' to a 3rd party API as a multipart/form-data file.")
			
			except Exception as e:
				print(f"     - Failed to process {file_url}: {e}")
		print("Finished processing files.\n")
	
	def finalize_run(self, processed_files: list[str]):
		"""
		Prints a final summary of the run and cleans up downloaded files.
		"""
		print("--- Step 6: Finalizing Run ---")
		print("Done")
		if processed_files:
			print("\nThe following new files were processed in this run:")
			for url in processed_files:
				print(f"  - {url}")
		else:
			print("\nNo new files were found to process in this run.")
		
		# Best practice: Clean up the temporary download directory
		print("\nCleaning up temporary download directory...")
		try:
			shutil.rmtree(self.download_dir)
			print(f"Successfully removed {self.download_dir}")
		except Exception as e:
			print(f"Error cleaning up directory '{self.download_dir}': {e}")


# --- Main Execution Logic ---
if __name__ == '__main__':
	# User will only provide the URL
	TARGET_URL = "https://rbi.org.in/home.aspx"

	# Initialize the processor
	processor = UrlCrawler(start_url=TARGET_URL)

	# --- Execute the modular workflow ---
	# 1. Process the main URL via a 3rd party service
	processor.process_initial_url_with_api()

	# 2. Get the list of files that are already known from another source.
	files_already_in_system = processor.get_files_from_external_source()

	# 3. Crawl the website to find all unique files currently on the site.
	all_files_on_site = processor.crawl_and_discover_files(max_pages=40)  # Small crawl for demo

	# 4. Compare the two lists to find only the truly new files to process.
	#    The comparison is based on the normalized filename.
	filenames_already_in_system = {processor._get_normalized_filename(url) for url in files_already_in_system}

	newly_added_files = []
	for url in all_files_on_site:
		if processor._get_normalized_filename(url) not in filenames_already_in_system:
			newly_added_files.append(url)

	print(f"--- Step 4: Comparing discovered files with existing files ---")
	print(f"Found {len(newly_added_files)} new files to be processed.\n")

	# 5. Process only the newly added files.
	processor.process_files_via_api(newly_added_files)

	# 6. Print a final summary and clean up temporary files.
	processor.finalize_run(newly_added_files)