from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scraper.items import DjangodashItem

from unidecode import unidecode


class DjangodashSpider(BaseSpider):
    name = 'dash'
    start_urls = [
        "http://djangodash.com/teams/c4/3f17/",
        "http://djangodash.com/teams/c4/6boxes/",
        "http://djangodash.com/teams/c4/amazingworks/",
        "http://djangodash.com/teams/c4/bitality/",
        "http://djangodash.com/teams/c4/blinken-bloop/",
        "http://djangodash.com/teams/c4/brainpanic/",
        "http://djangodash.com/teams/c4/changers/",
        "http://djangodash.com/teams/c4/clana-banana/",
        "http://djangodash.com/teams/c4/clockmakers/",
        "http://djangodash.com/teams/c4/codingmood/",
        "http://djangodash.com/teams/c4/crooked-horn/",
        "http://djangodash.com/teams/c4/cryptic-storms/",
        "http://djangodash.com/teams/c4/dashcoders/",
        "http://djangodash.com/teams/c4/dcr/",
        "http://djangodash.com/teams/c4/desbiz/",
        "http://djangodash.com/teams/c4/dev8/",
        "http://djangodash.com/teams/c4/devil-of-a-sub-sub-white-whale/",
        "http://djangodash.com/teams/c4/devpod/",
        "http://djangodash.com/teams/c4/e-legion/",
        "http://djangodash.com/teams/c4/egonomist/",
        "http://djangodash.com/teams/c4/esebe-labs/",
        "http://djangodash.com/teams/c4/evercodelab/",
        "http://djangodash.com/teams/c4/flaming-turkeys/",
        "http://djangodash.com/teams/c4/forthcoming/",
        "http://djangodash.com/teams/c4/future-colors/",
        "http://djangodash.com/teams/c4/gatsby/",
        "http://djangodash.com/teams/c4/gisthis/",
        "http://djangodash.com/teams/c4/hameedullah-salman/",
        "http://djangodash.com/teams/c4/hashcode/",
        "http://djangodash.com/teams/c4/hellfire/",
        "http://djangodash.com/teams/c4/ildus/",
        "http://djangodash.com/teams/c4/install-requires/",
        "http://djangodash.com/teams/c4/krkmetal/",
        "http://djangodash.com/teams/c4/lifeofpy/",
        "http://djangodash.com/teams/c4/mahou-shoujo-200apm/",
        "http://djangodash.com/teams/c4/maineiacs/",
        "http://djangodash.com/teams/c4/melbourne-warriors/",
        "http://djangodash.com/teams/c4/mentor-up/",
        "http://djangodash.com/teams/c4/mily/",
        "http://djangodash.com/teams/c4/mmoit/",
        "http://djangodash.com/teams/c4/mozfighters/",
        "http://djangodash.com/teams/c4/muffins-on-dope/",
        "http://djangodash.com/teams/c4/networky/",
        "http://djangodash.com/teams/c4/nsupdateinfo/",
        "http://djangodash.com/teams/c4/nvbn/",
        "http://djangodash.com/teams/c4/opensourcesaguenay/",
        "http://djangodash.com/teams/c4/ornumental/",
        "http://djangodash.com/teams/c4/papaconchoco/",
        "http://djangodash.com/teams/c4/pitombeiros/",
        "http://djangodash.com/teams/c4/platypi/",
        "http://djangodash.com/teams/c4/puccis/",
        "http://djangodash.com/teams/c4/pygeek/",
        "http://djangodash.com/teams/c4/pyjamas/",
        "http://djangodash.com/teams/c4/rebranch/",
        "http://djangodash.com/teams/c4/reddoid/",
        "http://djangodash.com/teams/c4/release-the-kraken/",
        "http://djangodash.com/teams/c4/roll-studio/",
        "http://djangodash.com/teams/c4/shultais-group/",
        "http://djangodash.com/teams/c4/sophilabs/",
        "http://djangodash.com/teams/c4/ssbb-vs-all/",
        "http://djangodash.com/teams/c4/the-clockmakers/",
        "http://djangodash.com/teams/c4/three-followers/",
        "http://djangodash.com/teams/c4/transcode/",
        "http://djangodash.com/teams/c4/travelog/",
        "http://djangodash.com/teams/c4/two-robots/",
        "http://djangodash.com/teams/c4/uncool-inc/",
        "http://djangodash.com/teams/c4/upchk/",
        "http://djangodash.com/teams/c4/valzevuls-team/",
        "http://djangodash.com/teams/c4/veikab/",
        "http://djangodash.com/teams/c4/vm-team/",
        "http://djangodash.com/teams/c4/wb-tech/",
        "http://djangodash.com/teams/c4/web-for-good/",
        "http://djangodash.com/teams/c4/webriders-duo/",
        "http://djangodash.com/teams/c4/webriders-uno/",
        "http://djangodash.com/teams/c4/ya-ma-kun/",
        "http://djangodash.com/teams/c4/yama-kun/",
        "http://djangodash.com/teams/c4/yamada/",
        "http://djangodash.com/teams/c4/yamakun/",
        "http://djangodash.com/teams/c4/yarp/",
        "http://djangodash.com/teams/c4/zapix/",
        "http://djangodash.com/teams/c4/guitar/"
    ]

    def __init__(self, *args, **kwargs):
        super(DjangodashSpider, self).__init__(*args, **kwargs)
        log.start()

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        item = DjangodashItem()
        repo = hxs.select('//div[@class="project_info"]//a[1]/text()').extract()[0]
        nicks = hxs.select('//div[@class="team_member"]//small/text()').extract()
        team = hxs.select('//section[@class="team_detail"]//header[1]/text()').extract()[0]
        item['repo'] = unidecode(repo)
        item['nicks'] = map(unidecode, nicks)
        item['team'] = unidecode(team)
        return item
