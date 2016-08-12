#coding:utf-8
import scrapy,json,re,os
from scrapy import Selector
from positionDetails.items import PositiondetailsItem
from bs4 import BeautifulSoup
basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class KeysSpider(scrapy.Spider):
    name = "lagou"
    allowed_domains = ["*.lagou.com"]
    start_urls = [
        "http://www.lagou.com/"
        ]

    def parse(self,response):
        keywords = [json.loads(line) for line in open(basedir + '/positionData/KeyWords.json')]
        next_url = "http://www.lagou.com/jobs/positionAjax.json?kd={}"
        for kd in keywords[0][u'技术'][0]:
            yield scrapy.FormRequest(next_url.format(kd.encode('utf-8')),callback=self.parse_json_link,meta={'kd':kd},dont_filter=True)

    def parse_json_link(self,response):
        kd = response.meta['kd']
        totalPageCount = json.loads(response.body_as_unicode())["content"]['totalPageCount']
        for page in range((int(totalPageCount))):
            yield scrapy.Request("{}&pn={}".format(response.url,page+1),callback=self.parse_id,meta={'kd':kd},dont_filter=True)

    def parse_id(self,response):
        kd = response.meta['kd']
        detail_url = "http://www.lagou.com/jobs/{}.html"
        json_response = json.loads(response.body_as_unicode())
        for id in json_response["content"]['result']:
            yield scrapy.Request(detail_url.format(id['positionId']),callback=self.parse_detail,meta={'kd':kd},dont_filter=True)

    def parse_detail(self,response):
        item = PositiondetailsItem()
        sel = Selector(response)

        try:
            item["positionName"] = self.get_text(sel,'//*[@id="job_detail"]/dt/h1/@title')
            item["company"] = sel.xpath('//*[@id="container"]/div[2]/d1/dt/h1/text()').extract().strip()
            item["city"] = sel.xpath('//*[@id="job_detail"]/dd[1]/p[1]/span[2]/text()').extract()[0]
            item["experience"] = sel.xpath('//*[@id="job_detail"]/dd[1]/p[1]/span[3]/text()').extract()[0]
            item["positionType"] = sel.xpath('//*[@id="job_detail"]/dd[1]/p[1]/span[4]/text()').extract()[0]
            item["salary"] = sel.xpath('//*[@id="job_detail"]/dd[1]/p[1]/span[1]/text()').extract()[0]
            item["description"] = self.get_text(sel,'//*[@id="job_detail"]/dd[2]')
            item["link"] = response.url
            item["publishedTime"] = sel.xpath('//*[@id="job_detail"]/dd[1]/p[3]/text()').extract()[0][:-8]
        except Exception, e:
            print e
        yield item

    def get_text(self,sel,path):
        xpath_text = sel.xpath(path).extract()[0]
        text = BeautifulSoup(xpath_text).get_text()
        text = re.sub(r'\n|\r|\t|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020|\\|"\"|\"', '', text)
        return text



