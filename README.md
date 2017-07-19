# XMarks Revisions Scraper

### Scrapes all revisions of your XMarks bookmarks, and optionally does additional processing and merging.

[XMarks](http://xmarks.com/) is a fairly good bookmark backup/share service, and I've been using it since 2012.  Once upon a time, I accidentally deleted and then synchronized my bookmarks.  Fortunately, XMarks stores revisions of your bookmarks, but unfortunately I didn't realize I had screwed up until some time later, when I had added more bookmarks.

To fix this, one should download all the revisions, merge all URLs in them, and then re-upload.  Unfortunately, XMarks had 2264 revisions of my bookmarks and a messy JavaScript GUI to download them individually, but not (despite my support request) a way to download them collectively.

Hence, these scripts.  These will scrape the website and allow you to download all revisions of your bookmarks.  I had a hard time reverse-engineering everything, and the result is rather brittle and unsatisfactory.  But, it worked for me (and maybe will for you!).

## Instructions

1. Install prerequisites
    1. Install [Python](https://www.python.org/downloads/).  These scripts were tested with Python 3.5.1, but other Python 3s should work.
    2. Install `lxml` and `pyparsing`.  Pip works fine:<br/>
    `pip install --upgrade lxml pyparsing`<br/>
    If it's not on your `PATH`, then point to it.  On Windows, this is something like (check the actual location):<br/>
    `C:\Python35\Scripts\pip.exe install --upgrade lxml pyparsing`

2. Extract the revision list.
    1. Go to [https://www.xmarks.com/](https://www.xmarks.com/).  Click "LOG IN" and log in, as-necessary.
    2. Click "MY BOOKMARKS".  This starts their GUI.
    3. Click "Tools -> Export & Restore Old Bookmarks...".  A window displaying a list of revisions appears.
    4. Inside the list of revisions, inspect an element (this gets the page source *after* JavaScript processing has messed with it).
    5. In the source, you should see a table, id `revisions_table`, with child `<tbody>`.  Copy the `<tbody>` outer HTML (i.e., including `<tbody>` itself into a new text file "revs-table.xml").

3. Convert the revisions table into URLs to scrape.
    1. Run "3.-get-urls.py".  This takes "revs-table.xml" and uses it to produce a new file, "revs-urls.txt".

4. Scape all revisions.
    1. Open "4.-crawler.py".  Set your username and password.
    2. Run "4.-crawler.py".  This takes "revs-urls.txt" and downloads it into "revisions/*.html".
    3. The scrape sometimes fails (because the server fails).  The result is a 1 KB file saying that something failed.  In these cases, simply delete the failed file(s) and repeat the previous sub-step (already-downloaded files will be skipped).

5. Merge revisions:

    1. Run "5.-merge.py".  This takes the "revisions/*.html" files and outputs "combined-bookmarks.html", which is suitable to re-upload to XMarks.  Since this can take a while and has the highest probability of failure, it checkpoints every ten merges into "tmp/".

## Problems

Please read the directions.  As noted, you need to install prerequisites, create a new file, and make a few source-level changes.

There may additionally exist minor issues; the code was in some cases edited after initial testing and it's possible I screwed up.  On the whole it should work alright, with perhaps minor changes (which I'd like to hear about).

There may additionally exist major issues.  The code is brittle, and may not work for your particular case.  Or perhaps XMarks will change their website.  If you can't figure something out, contact me, and I'll see if maybe it can be fixed easily.  Python 2 is not supported, although you are welcome to add support for it.

## Credits

I did all of the poking around work trying to reverse-engineer XMarks's API.  This was difficult, since I don't know what I'm doing.  After some false leads, when a test download actually failed, I was able to get the actual URL format.

The scraper is an adapted version of [this wonderful example](https://github.com/kazuar/login_scraper_example).

The merger is essentially "[bookmark-merger](http://bookmark-merger.sourceforge.net/)", although I ran it through "2to3.py", cleaned the result up, and fixed a few things (the parser is not very robust, so some initial efforts failed).  The result is redistributed here, in accordance with its LGPL license.

I used [this](https://stackoverflow.com/a/7265260/688624) as an additional reference while writing initial parsers.  Various others for various smaller tasks.