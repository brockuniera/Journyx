import json
import re
import urllib.request

__RE_HTMLTITLE = re.compile(r'<title>(.{0,150})</title>')

def titleFromURL(url: str) -> str:
    """
    given a url, download its webpage and return its title, or "" if there was a problem
    """
    try:
        page = urllib.request.urlopen(url)
    except:
        return ""
    if not page:
        return ""

    html = str(page.read())

    # parse html to get a title
    title = __RE_HTMLTITLE.search(html)
    return title.group(1) if title else ""

__RE_MENTION = re.compile(r'@(\w+)')
__RE_URL = re.compile(r'http')
__RE_EMOTICON = re.compile(r'\((\w{1,15})\)')

def processString(chatstr: str) -> str:
    """
    Takes a chat message string and returns a JSON string containing information
    about its contents. You should look for the following features:

    1) @mentions - This is a way to mention another user. They always start with '@'
        and end when hitting a non-word character.
    2) Links - any URLs that are contained in the message, plus the page's current
        title up to 200 characters. You can assume that all URLs start with http.
    3) Emoticons - for this exercise, you can assume that emoticons are defined as any
        alphanumeric string, no longer than 15 characters with no whitespace,
        contained in parenthesis.
    4) An integer word count of remaining words, not counting any @mentions, links, or
        emoticons.
    """

    mentions = []
    links = []
    emoticons = []
    words = 0

    def mentionHandler(word):
        mention = __RE_MENTION.match(word)
        if mention:
            mentions.append(mention.group(1))
            return True
        return False

    def linksHandler(word):
        url = __RE_URL.match(word)
        if url:
            title = titleFromURL(word)
            links.append({
                'url': word,
                'title': title
                })
            return True
        return False

    def emoticonsHandler(word):
        emote = __RE_EMOTICON.match(word)
        if emote:
            emoticons.append(emote.group(1))
            return True
        return False

    handlers = [mentionHandler, linksHandler, emoticonsHandler]

    stripwords = (w.strip() for w in chatstr.split(' '))
    for word in stripwords:
        if len(word) == 0:
            continue

        for func in handlers:
            if func(word):
                break
        else:
            words += 1

    # Only include nessacary properties on resdict
    resdict = {'words': words}
    if mentions: resdict['mentions'] = mentions
    if links: resdict['links'] = links
    if emoticons: resdict['emoticons'] = emoticons
    return json.dumps(resdict)

if __name__ == "__main__":
    print(processString("hey what's up (smile) @john? http://google.com"))
