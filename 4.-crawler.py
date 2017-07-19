import requests
from lxml import html
import os


USERNAME = "<YOUR-XMARKS-USERNAME-HERE>"
PASSWORD = "<YOUR-XMARKS-PASSWORD-HERE>"

#You should set the variables.
assert USERNAME != "<YOUR-XMARKS-USERNAME-HERE>"
assert PASSWORD != "<YOUR-XMARKS-PASSWORD-HERE>"

def download_rev(session, url):
    name = url.split("/")
    rev = name[-2]
    xmarks,bookmarks,year,month,day_dot_html = name[-1].split("-")
    day = day_dot_html.split(".")[0]
    name = "bookmarks-%04d-%02d-%02d-rev-%06d.html" % (int(year),int(month),int(day),int(rev))
    path = "revisions/" + name

    if os.path.exists(path):
        print("Skipping URL for rev %s (file already exists)"%(rev))
    else:
        print("Scraping URL for rev %s"%(rev))

        # Scrape url
        result = session.get(
            url,
            headers=dict(referer=url)
        )

        f = open(path,"wb")
        f.write(result.content)
        f.close()

def main():
    #Figure out which URLs to crawl (run "get-urls.py" if this file doesn't exist)
    print("Attemping to load URLs . . .")
    file = open("revs-urls.txt","r")
    urls = file.readlines()
    for i in range(len(urls)):
        urls[i] = urls[i].strip()
    file.close()
    print("Loaded %d URLs"%(len(urls)))

    #Open SSL session.
    print("Opening SSL session . . .")
    session = requests.session()

    url_login = "https://login.xmarks.com/"

    #Get login CSRF token
    print("Getting CSRF security token . . .")
    result = session.get(url_login)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='token']/@value")))[0]

    #Perform login
    print("Logging in . . .")
    payload = {
        "username": USERNAME, 
        "password": PASSWORD, 
        "token": authenticity_token
    }
    result = session.post(url_login, data=payload, headers=dict(referer=url_login))

    #Download revisions
    print("Preparing to scrape requested URLs . . .")
    for url in urls:
        download_rev(session, url)

if __name__ == '__main__':
    main()
