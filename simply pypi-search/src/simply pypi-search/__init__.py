from bs4 import BeautifulSoup
from aiohttp import ClientSession

usr_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/61.0.3163.100 Safari/537.36'}

class PyPiSearch:
    def __init__(self):
        self.search = self.pypi_search
    @classmethod
    async def pypi_search(cls, keyword: str)->list:
        """
        Returns an :class:`list` with :class:`PyPiProject` 's of the search

        :param keyword:
        :return: [result1, result2, result3, etc.]
        """
        html = await cls().pypi_get_results(keyword)
        return list(cls().parse_pypi_results(html))
    
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
            link = result.find('a', href=True)['href']
            name = result.find('span', attrs={'class': 'package-snippet__name'})
            version = result.find('span', attrs={'class': 'package-snippet__version'})
            description = result.find('p', attrs={'class': 'package-snippet__description'})
            release = result.find('time').decode_scontents().strip("\n \n")
            if name is not None:
                name = name.decode_contents()
            if version is not None:
                version = version.decode_contents()
            if description is not None:
                description = description.decode_contents()
            if name and link:
                yield PyPiProject({"name": name, "description": description, "version": version, "released": release, "link": "https://pypi.org"+link})




class PyPiProject:
    """
    The Objekt that a :func:`~PyPiSearch.pypi_search` returns

    :class: PyPiProject

    """
    def __init__(self, data: dict):
        self.Name =  data.get('name')
        self.Description: str = data.get('description')
        self.Version: str = data.get('version')
        self.Released: str = data.get('released')
        self.Link: str = data.get('link')

    @property
    def name(self):
        return self.Name
    @property
    def description(self):
        return self.Description
    @property
    def version(self):
        return self.Version
    @property
    def released(self):
        return self.Released
    @property
    def link(self):
        return self.Link
