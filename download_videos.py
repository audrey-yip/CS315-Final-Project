import pyktok as pyk
import logging
import time

def download_tiktok_mp3s(urls):
    logger = logging.getLogger()
    file_handler = logging.FileHandler('download_failures.log')
    logger.addHandler(file_handler)

    pyk.specify_browser('chrome')
    for url in urls:
        try:
            pyk.download_tiktok_audio(url)
            time.sleep(3)
        except Exception as exc:
            logger.warning("error while processing item: %s", exc)

    return True

if __name__ == "__main__":
    download_tiktok_mp3s(['https://www.tiktokv.com/share/video/7315561816673750318/'])