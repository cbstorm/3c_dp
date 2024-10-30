FPS=1
.PHONY: $(shell ls .)
dl:
	youtubedr download --quality hd720 --mimetype mp4 -o ./videos/$(FNAME).mp4 $(URL)
info:
	youtubedr info $(URL)
crop:
	ffmpeg -i ./videos/$(FNAME).mp4 -vf "crop=$(W):$(H):$(X):$(Y)" ./videos/$(FNAME)_c.mp4
cut:
	ffmpeg -ss $(FROM) -to $(TO) -i ./videos/$(FNAME).mp4 -c:v copy ./videos/$(FNAME)_$(FROM)_$(TO).mp4
view:
	python3 v_view.py ./videos/$(FNAME).mp4
rotate:
	ffmpeg -i ./videos/$(FNAME).mp4 -vf "transpose=1" ./videos/$(FNAME)_r.mp4
extract:
	ffmpeg -i ./videos/$(FNAME).mp4 -vf "fps=$(FPS)" -q:v 1 ./images/$(FNAME)_%06d.jpg
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
s_view:
	python3 v_view.py $(FNAME)
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
mvclsmodel:
	mkdir -p models/cls/$(shell date +%s)
	cp runs/classify/train/weights/best.pt models/cls/$(shell date +%s)/best.pt
	cp runs/classify/train/results.csv models/cls/$(shell date +%s)/
	

