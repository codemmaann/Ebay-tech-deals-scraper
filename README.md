# Ebay-tech-deals-scraper

## Methodology
1. **Web Scraping**: Used Selenium to scrape eBay's Global Tech Deals page
2. **Automation**: GitHub Actions runs the scraper every 3 hours
3. **Data Cleaning**: Processed raw data, handled missing values, calculated discounts
4. **EDA**: Analyzed patterns in pricing, discounts, and product categories

## Key Findings
- Most deals are scraped during [hours based on your data]
- Price distribution shows [patterns from your data]
- Top discounts reach up to [max discount percentage]%
- Most common keywords in titles: [top keywords from your data]

## Challenges
- Dynamic content loading required careful scrolling implementation
- Price formatting inconsistencies needed robust cleaning
- GitHub Actions setup for scheduled scraping

## Potential Improvements
- Add more sophisticated product categorization
- Implement price tracking over time
- Add sentiment analysis on product reviews
- Expand to multiple eBay categories