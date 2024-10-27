from lib import lbstudio
import urllib.request


def Download(f_name):
    lbstudio.client.files.download(filename=f_name)


def HttpDownload(f_name):
    url = "{LABEL_STUDIO_URL}/data/upload/1/{f_name}".format(
        LABEL_STUDIO_URL=lbstudio.LABEL_STUDIO_URL, f_name=f_name)
    dst = "tmp/{f_name}".format(f_name=f_name)
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('Authorization', 'Token {LABEL_STUDIO_APIKEY}'.format(
            LABEL_STUDIO_APIKEY=lbstudio.LABEL_STUDIO_APIKEY))
    ]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, dst)
