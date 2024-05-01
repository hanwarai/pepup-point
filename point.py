from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os

# secretsに登録した環境変数の呼び出し
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # ログインページ
    page.goto("https://pepup.life/users/sign_in")

    # ユーザ名、パスワードをセット
    page.get_by_placeholder('登録したEメールアドレス').fill(USERNAME)
    page.get_by_placeholder('8文字以上のパスワード').fill(PASSWORD)
    page.get_by_role("button", name="ログイン").click()

    for num in range(1, 3):

        # 健康記事
        page.goto("https://pepup.life/articles?page=" + str(num))

        # 健康記事の一覧
        ul = page.inner_html('ul[data-testid="article-list"]')
        soup = BeautifulSoup(ul, 'html.parser')

        # ポイントのある記事
        for article in soup.find_all('a'):
            href = article.get('href')
            div_points = article.css.select('div[data-testid="article-points"]')

            if len(div_points) > 0:
                print(href)

                # ポイントゲット
                page.goto('https://pepup.life' + href)
                page.get_by_role("button", name="参考になった").click()
                page.get_by_role("button", name="ポイントをもらう！").click()

    browser.close()
