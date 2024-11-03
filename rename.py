import os
import sys
from lib.file import SortedAlphanumeric
import time
dir = sys.argv[1]

files = SortedAlphanumeric(os.listdir(dir))

for fi in files:
    old_p = os.path.join(dir, fi)
    n, ext = os.path.splitext(os.path.basename(fi))
    new_p = os.path.join(dir, n + str(time.time()) + ext)
    os.system("mv {old_p} {new_p}".format(old_p=old_p, new_p=new_p))
