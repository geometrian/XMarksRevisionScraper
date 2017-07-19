from xml.etree import ElementTree
import io



#Have to do some string processing on the HTML copied by the user, to fix it up.
#   Load data.  If fails, probably because this file doesn't exist.  Follow the
#   directions in the README.
print("Attempting to load revisions table . . .")
file = open("revs-table.xml","r")
data = file.read()
file.close()
#   The `<input ...>` tags are not correctly closed.  Hackish fix.
print("Fixing broken `<input ...>` tags . . .")
data = data.replace("type=\"radio\">","type=\"radio\"></input>")
#   Preprend some XML stuff, because the parser apparently needs it.
print("Prepending parse info. . . .")
data = """<!DOCTYPE reasonable [
    <!ENTITY nbsp "&#0160;">
]>
"""+data
#   Wrap it in a file IO wrapper so the parser can handle it.
print("Preparing parser IO . . .")
str_file = io.StringIO(data)

#Parse file
print("Parsing table . . .")
et = ElementTree.ElementTree()
root = et.parse(str_file)

#Extract revision numbers/dates
print("Extracting revision numbers/dates . . .")
revs = []
date = None
for tr in root[1:]:
    assert tr.tag == "tr"

    td_rev = tr[1]
    assert "revision-number" in td_rev.attrib.values()
    rev_num = int(td_rev.text)

    td_date = tr[2]
    assert "revision-date" in td_date.attrib.values()
    rev_date = td_date.text
    if rev_date == "\xa0": #&nbsp;
        rev_date = date #Propagate from previous
    else:
        rev_date = rev_date.strip().split("/")
        rev_date = [int(rev_date[2]),int(rev_date[0]),int(rev_date[1])]
        date = rev_date

    revs.append((rev_num,rev_date))

#Write out the URLs we need to crawl.
print("Outputting URLs . . .")
file = open("revs-urls.txt","w")
for rev_num,rev_date in revs:
    year,month,day = rev_date
    file.write("https://my.xmarks.com/bookmarks/export_to_html/%d/xmarks-bookmarks-%04d-%02d-%02d.html\n"%(rev_num,year,month,day))
file.close()

print("Complete!")
