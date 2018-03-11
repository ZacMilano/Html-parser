from urllib.request import urlopen
from bs4 import BeautifulSoup
import bs4

class ParsedText():
  '''
  A class for extracting all visible text from an HTML file into a string.

  If desired, this can all be turned into one large function.
  '''

  def __init__(self, url, also_remove=[]):
    '''Constructor for ParsedText objects.

    Parameters
    ----------
    url : string
      The URL of the desired HTML document.
    also_remove : list
      A list of the names of other possible HTML tags, in string form, whose
      content/text should not be included (ex: also_remove=['p', 'table', 'div']).
      This list is appended onto self.disallowed_tags, the initial list of tags to
      remove from the results.

    Product
    -------
    ParsedText
      A ParsedText object instance.
    '''
    self.url = url
    self.disallowed_tags = [
      '[document]',
      'head',
      'meta',
      'script',
      'style',
      'title'
    ]
    for tag in also_remove:
      self.disallowed_tags.append(tag)

  def element_is_visible(self, elmt):
    '''Filter method for choosing which elements to keep from the HTML. Comments
    and the contents of self.disallowed_tags are removed.

    Parameters
    ----------
    elmt : string
      A string whose value is the name of an HTML tag.

    Returns
    -------
    boolean
      False if the element should NOT be included, otherwise true.
    '''
    if isinstance(elmt, bs4.element.Comment):
      return False
    if elmt.parent.name in self.disallowed_tags:
      return False
    return True

  def get_text(self, url=None, parsing_style='html.parser'):
    '''Get the actual visible text from the document.

    PROBLEMS
    --------
    I'm not sure if this is actually a problem, but I have this configured to
    return unicode text, so some specific symbols (em dash, copyright symbol,
    etc.) might not appear properly in some cases.

    Parameters
    ----------
    url : string
      The URL of the desired HTMl document.
    parsing_style : string
      How the text should be parsed.
      Restrictions on the value of parsing_style can be found at
      https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser

    Returns
    -------
    string
      A long string with all the visible text from the webpage.
    '''
    if url is None:
      url = self.url

    html = urlopen(url).read()

    soup = BeautifulSoup(html, parsing_style)
    text_fields = soup.findAll(text=True)
    visible_text_fields = filter(self.element_is_visible, text_fields)
    return u' '.join(vis_txt.strip() for vis_txt in visible_text_fields)

# This is an example that I used for testing.
# a = ParsedText('http://docs.sqlalchemy.org/en/latest/core/event.html')
# print(a.get_text())
