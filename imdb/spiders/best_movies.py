import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = "best_movies"
    allowed_domains = ["imdb.com"]

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.imdb.com/chart/top/",
            headers={"User-Agent": self.user_agent},
        )

    def set_user_agent(self, request):
        request.headers["User-Agent"] = self.user_agent
        return request

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths='//li//a[@class="ipc-title-link-wrapper"]'),
            callback="parse_item",
            follow=True,
            # process_request="set_user_agent",
        ),
    )

    def parse_item(self, response):
        yield {
            "header": response.xpath("//h1/span/text()").get(),
            "year": response.xpath(
                '(//li[@class="ipc-inline-list__item"]/a[@class="ipc-link ipc-link--baseAlt ipc-link--inherit-color"])[5]/text()'
            ).get(),
            "duration": response.xpath(
                '(//li[@class="ipc-inline-list__item"])[7]/text()'
            ).get(),
            "genere": response.xpath(
                '//a[@class="ipc-chip ipc-chip--on-baseAlt"]/span/text()'
            ).get(),
            "rating": response.xpath(
                '(//span[@class="sc-bde20123-1 cMEQkK"])[2]/text()'
            ).get(),
            "movie_url": response.url,
        }
