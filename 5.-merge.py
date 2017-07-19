import os
#`C:/dev/Python35/Tools/scripts/2to3.py -w bookmark_pyparser.py`, plus manual cleanup.
import _bookmark_pyparser as bpp


print("Getting paths . . .")

def get_files(directory):
    paths = [directory+f for f in os.listdir(directory) if os.path.isfile(directory+f)]
    return paths

def load_from(file):
    parsed_file = bpp.bookmarkshtml.parseFile(open(file,"r",encoding="utf8"))
    parsed_dict = bpp.bookmarkDict(parsed_file)
    return parsed_dict
def save_to(file, result):
    merged_file = open(file,"w",encoding="utf8")
    merged_file.write( bpp.serialize_bookmarkDict(result) )
    merged_file.close()

##load_from("test.html")

tmps = get_files("tmp/")
if len(tmps) > 0:
    print("Attempting to load from partial cache . . .")
    result = load_from(tmps[-1])
    next_i = int( os.path.basename(tmps[-1]).split(".")[0] ) + 1
    print("Skipped successfully to index "+str(next_i)+"!")
else:
    result = {}
    next_i = 0

paths = get_files("revisions/")
for i in range(next_i,len(paths),1):
    print("Loading and merging file %d \"%s\" . . ."%(i,paths[i]))

    parsed_dict = load_from(paths[i])
    result = bpp.merge_bookmarkDict(result,parsed_dict)

    if i>0 and i%10==0:
        print("Saving temp \"%s\" . . ."%paths[i])
        save_to("tmp/%06d.html"%i,result)

print("Writing result . . .")
save_to("combined-bookmarks.html",result)

print("Complete!")
