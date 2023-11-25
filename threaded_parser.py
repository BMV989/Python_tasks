import argparse
import os
import pathlib
import re
import signal
import sys
import urllib.request
import threading
from typing import Optional
from urllib.error import URLError, HTTPError

HABR = "https://habr.com"
RE_IMAGES = re.compile(r'<img src=\"')


def correct_name_folder(name):
    invalid_chars = r'\/:*?<>|'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name


def load_content(url: str) -> Optional[bytes]:
    try:
        return urllib.request.urlopen(url, timeout=10).read()
    except (HTTPError, URLError):
        return None


def get_images(article_link):
    content = load_content(f"{HABR}{article_link}").decode("utf-8")
    if content is None:
        return
    body_start = content.find(r'<div id="post-content-body">')
    body_end = content.find(r'</div>', body_start)
    inner_content = content[body_start:body_end]
    all_images = RE_IMAGES.finditer(inner_content)
    images = []
    for image in all_images:
        start_ref = image.end()
        end_ref = inner_content.find(r'"', start_ref)
        images.append(inner_content[start_ref:end_ref])
    return images


def download_images(name_article, article_link):
    images = get_images(article_link)

    if not images:
        return

    name_article = correct_name_folder(name_article)
    os.makedirs(name_article, exist_ok=True)

    for ref in images:
        image_content = load_content(ref)
        if image_content is None:
            return
        image_name = ref[ref.rfind('/') + 1:]
        path = os.path.join(name_article, image_name)
        with open(path, "wb") as img:
            img.write(image_content)


class GracefulShutdown:
    def __init__(self, thread):
        self.threads = thread
        self.event = threading.Event()
        signal.signal(signal.SIGINT, self.exit_graceful)
        signal.signal(signal.SIGTERM, self.exit_graceful)

    def exit_graceful(self, signum, frame):
        self.event.set()
        self.wait_threads(self.threads)

    @staticmethod
    def wait_threads(threads):
        while threads:
            threads.pop().join()


def run_scraper(threads: int, articles: int, out_dir: pathlib.Path) -> None:
    thread_pool = []
    gs = GracefulShutdown(thread_pool)

    if not (os.path.exists(out_dir)):
        os.makedirs(out_dir, exist_ok=True)
    os.chdir(out_dir)

    content = load_content(HABR).decode("utf-8")
    re_headers = re.compile(r'<h2.*<\/h2>')
    re_name = re.compile(r'<span>(.*)<\/span>')
    re_href = re.compile(r'<a href=\"(.*)\"')
    article_list = re.findall(re_headers, content)[:articles]

    for lnk in article_list:
        if gs.event.is_set():
            break
        while len(thread_pool) >= threads:
            for thread in thread_pool:
                if not thread.is_alive():
                    thread_pool.remove(thread)
                    break

        article_name = re.search(re_name, lnk).group(1)
        article_link = re.search(re_href, lnk).group(
            1)
        article_link = article_link[:article_link.find(r'"', 1)]
        thread = threading.Thread(
            target=download_images(article_name, article_link))
        thread_pool.append(thread)
        thread.start()
    GracefulShutdown.wait_threads(thread_pool)


def main():
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        usage=f'{script_name} [ARTICLES_NUMBER] THREAD_NUMBER OUT_DIRECTORY',
        description='Habr parser',
    )
    parser.add_argument(
        '-n', type=int, default=25, help='Number of articles to be processed',
    )
    parser.add_argument(
        'threads', type=int, help='Number of threads to be run',
    )
    parser.add_argument(
        'out_dir', type=pathlib.Path, help='Directory to download habr images',
    )
    args = parser.parse_args()

    run_scraper(args.threads, args.n, args.out_dir)


if __name__ == '__main__':
    main()
