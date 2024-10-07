from crewai_tools import SerperDevTool
from crewai_tools import SeleniumScrapingTool

# Initialize the tool for internet searching capabilities
url_extractor_tool = SerperDevTool()
scraper_tool=SeleniumScrapingTool()