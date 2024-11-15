FPS=1
.PHONY: $(shell ls .)
dl:
	youtubedr download --quality hd720 --mimetype mp4 -o ./videos/$(FNAME).mp4 $(URL)
info:
	youtubedr info $(URL)
crop:
	ffmpeg -i ./videos/$(FNAME).mp4 -vf "crop=$(W):$(H):$(X):$(Y)" ./videos/$(FNAME)_c.mp4
W=400
H=165
X=100
Y=60
crop_score_board:
	ffmpeg -i ./videos/$(FNAME).mp4 -map 0 -vf "crop=$(W):$(H):$(X):$(Y)" ./videos/$(FNAME)_score_board.mp4
cut:
	ffmpeg -ss $(FROM) -to $(TO) -i ./videos/$(FNAME).mp4 -map 0 -c:v copy ./videos/$(FNAME)_$(FROM)_$(TO).mp4
rotate:
	ffmpeg -i ./videos/$(FNAME).mp4 -vf "transpose=1" ./videos/$(FNAME)_r.mp4
extract:
	ffmpeg -i ./videos/$(FNAME).mp4 -vf "fps=$(FPS)" -q:v 1 ./images/$(FNAME)_$(shell date +%s)_%06d.jpg
filter:
	python3 filter.py
clean:
	rm -rf images/*
	rm -rf tmp/*
	rm -rf videos/*
	rm -rf runs
	rm -rf __dataset
	rm -rf dataset
	rm -rf runs
	rm -rf yolo* || true
	rm -rf 3c.yaml
view:
	python3 v_view.py videos/$(FNAME).mp4
s_view:
	python3 v_view.py $(FNAME)
view_cls:
	mkdir -p images/top
	mkdir -p images/not_top
	python3 view_cls.py ./videos/$(FNAME).mp4
v_info:
	python3 v_info.py videos/$(FNAME).mp4
n_view:
	python3 normal_view.py videos/$(FNAME).mp4
pred:
	python3 pred.py
lstasks:
	python3 lstasks.py
deps:
	pip3 freeze > requirements.txt
install:
	pip3 install -r requirements.txt
train:
	python3 train.py
train_classify:
	rm -rf dataset || true
	python3 train_classify.py
mvmodel:
	mkdir -p models/od/$(shell date +%s)
	cp runs/detect/train/weights/best.pt models/od/$(shell date +%s)/best.pt
	cp runs/detect/train/results.csv models/od/$(shell date +%s)/
mvbannermodel:
	mkdir -p models/banner/$(shell date +%s)
	cp runs/detect/train/weights/best.pt models/banner/$(shell date +%s)/best.pt
	cp runs/detect/train/results.csv models/banner/$(shell date +%s)/
mvclsmodel:
	mkdir -p models/cls/$(shell date +%s)
	cp runs/classify/train/weights/best.pt models/cls/$(shell date +%s)/best.pt
	cp runs/classify/train/results.csv models/cls/$(shell date +%s)/
dl_hls:
	hls_downloader -url=$(U) -path=$(P) -playlist=playlist.m3u8 -start=$(S) -end=$(E) -out=videos/vid_0.ts
mp4:
	ffmpeg -i videos/vid_0.ts -map 0 -acodec copy -vcodec copy videos/vid_0.mp4
top_log:
	mkdir -p tmp/vid_0
	python3 top_log.py videos/$(FNAME).mp4
concat:
	ffmpeg -f concat -safe 0 -i $(F) -map 0 -c copy videos/$(O).mp4
rename:
	python3 rename.py $(D)
thumb:
	python3 thumbnail.py videos/$(FNAME).mp4 $(T)
move_log:
	python3 move_log.py videos/$(FNAME).mp4

FACTOR = 1
score_log:
	python3 score_log.py videos/$(FNAME).mp4 $(FACTOR) > tmp/score_log.txt
read_score_log:
	mkdir -p tmp/$(FNAME)
	python3 read_score_log.py tmp/score_log.txt videos/$(FNAME).mp4
	ffmpeg -f concat -safe 0 -i tmp/vid_list.txt -c copy videos/vid_merge.mp4
train_banner:
	python3 train_banner.py
banner_view:
	python3 banner_view.py videos/$(FNAME).mp4
hide_banner:
	python3 hide_banner.py videos/$(FNAME).mp4
simple_hide_banner:
	# python3 simple_hide_banner.py videos/$(FNAME).mp4
	ffmpeg -i videos/$(FNAME).mp4 -filter_complex "[0:v]crop=1420:60:520:970,avgblur=20[fg];[0:v][fg]overlay=520:970[v]" -map "[v]" -map 0:a -c:v libx264 -c:a copy -movflags +faststart videos/$(FNAME)_hidden_banner.mp4