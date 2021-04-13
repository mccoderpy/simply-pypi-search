from bs4 import BeautifulSoup
from aiohttp import ClientSession

usr_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/61.0.3163.100 Safari/537.36'}

class Search:
    def __init__(self):
        __all__ =  {"pypi_search"}

    async def pypi_get_results(self, keyword):
        search_term = keyword.replace(" ", "+")
        async with ClientSession(headers=usr_agent) as suche:
            such_ergebnis = await suche.get(url=f"https://pypi.org/search/?q={search_term}&o")
            such_ergebnis.raise_for_status()
            results = await such_ergebnis.text()
        return results

    def parse_pypi_results(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        ul = soup.find('ul', attrs='unstyled')
        result_block = ul.find_all('li')
        for result in result_block:
            link = result.find('a', href=True)
            name = result.find('span', attrs={'class': 'package-snippet__name'})
            version = result.find('span', attrs={'class': 'package-snippet__version'})
            description = result.find('p', attrs={'class': 'package-snippet__description'})
            release = result.find('time').decode_contents()
            if name is not None:
                name = name.decode_contents()
            if version is not None:
                version = version.decode_contents()
            if description is not None:
                description = description.decode_contents()
            if name:
                yield SearchResult({"name": name, "description": description, "version": version, "released": release, "link": "https://pypi.org"+link['href']})

    @classmethod
    async def pypi_search(cls, keyword: str) -> list:
        """
        Returns an list of dicts with results of the search

        :class: Search
        :param keyword:
        :return: list[dict{name, description, version, release-time, link}]
        """
        html = await cls().pypi_get_results(keyword)

        return list(cls().parse_pypi_results(html))


class SearchResult:
    def __init__(self, data: dict):
        self.name: str = data.get('name')
        self.description: str = data.get('description')
        self.version: str = data.get('version')
        self.released: str = data.get('released')
        self.link: str = data.get('link')
