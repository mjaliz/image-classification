from scrapper import ImageScrapper

terms = []

with open('search_terms.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        terms.append(line.strip("\n"))

output_f = 'rejected-scraped'

for term in terms:
    scraper = ImageScrapper(term, output_f)
    scraper.scrape()
