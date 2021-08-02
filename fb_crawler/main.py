from fb_crawler.fb_class import FaceBookCrawler
from fb_crawler.utils import Utils


def main():
    fb_url = [
        "https://m.facebook.com/pg/1314ichiayi/posts/",
        "https://m.facebook.com/pg/taiwango0527/posts/",
        "https://m.facebook.com/wang.huimei/",
        "https://m.facebook.com/pg/pan.menan1/posts/",
        "https://m.facebook.com/pg/happiness.miaoli/posts/",
        "https://m.facebook.com/pg/yunlin.lishan/posts/",
    ]

    name = [
        "嘉義",
        "新竹",
        "彰化",
        "屏東",
        "苗栗",
        "雲林",
    ]
    util = Utils()
    util.create_dirs()
    for index, url in enumerate(fb_url):
        index = FaceBookCrawler(url, name[index], util)
        index.run()


if __name__ == "__main__":
    main()
