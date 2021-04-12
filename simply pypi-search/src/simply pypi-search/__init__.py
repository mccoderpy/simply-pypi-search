import multidict
from bs4 import BeautifulSoup
from aiohttp import ClientSession


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
                yield {"name": name, "description": description, "version": version, "release-time": release, "link": "https://pypi.org"+link['href']}

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
