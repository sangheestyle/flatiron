import sys
from repo import Repo

r = Repo()
r.read_repo(sys.argv[1], 5)
print len(r)
for commit in r:
    print commit
