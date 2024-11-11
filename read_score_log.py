import os
import sys
import re

LOG_PATH = sys.argv[1]
VID_PATH = sys.argv[2]
VID_NAME = os.path.splitext(os.path.basename(VID_PATH))[0]


def is_continous(t, prev_t):
    if t - prev_t == 1:
        return True
    return False


t_re = r"t=\s\d+"
pause_lines = []
with open(LOG_PATH, "r") as f:
    for l in f:
        if "Pause" in l:
            pause_lines += [l]

pause_range = []
start = -1
prev_t = -1
for l in pause_lines:
    t = re.findall(t_re, l)[0]
    t_n = int(t.split("= ")[1])
    if start == -1:
        start = t_n
    if not is_continous(t_n, prev_t) and prev_t != -1:
        pause_range += [[start, prev_t]]
        start = t_n
    prev_t = t_n

for r in pause_range:
    start = r[0] - 5
    end = r[1]
    os.system(
        "ffmpeg -ss {r0} -to {r1} -i {vid_path} -map 0 -c:v copy tmp/{vid_name}/{vid_name}_{r0}_{r1}.mp4".format(r0=start, r1=end, vid_path=VID_PATH, vid_name=VID_NAME))

command = "ls tmp/vid_0 | sort -V"
result = os.popen(command).read()
vid_list_f = open("tmp/vid_list.txt", "a")
for fi in result.split("\n"):
    if fi == "":
        continue
    vid_list_f.write("file './vid_0/{}'\n".format(fi))
f.close()
os.system(
    "ffmpeg -f concat -safe 0 -i ./tmp/vid_list.txt -c copy ./videos/vid_merge.mp4")
