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
	ffmpeg -i ./videos/$(FNAME).mp4 -vf "fps=1" -q:v 1 ./images/$(FNAME)_%06d.jpg
clean:
	rm -rf images/*
	rm -rf tmp/*
	rm -rf videos/*
	rm -rf runs
s_view:
	python3 v_view.py "srt://34.142.173.129:6000?streamid=/live/STR66FB56CF1?key=xExJSJGVcyBahJnQf7rlYwGhwiQ5m-"
pred:
	python3 pred.py
lstasks:
	python3 lstasks.py
deps:
	pip3 freeze > requirements.txt
install:
	pip3 install -r requirements.txt
	

