# crawlingHatenaBlog

## 環境構築
```
# インストール
pip install -r requirements.txt

# 仮想環境
source venv/bin/activate

# ファイルの実行
python crawl_HatenaBlog.py
```

# 使い方
## はてなブログのブログ記事をクローリング
- このようなページの記事をクロールする　http://b.hatena.ne.jp/entrylist?url=https%3A%2F%2Fjapanese.engadget.com%2F
- サンプルURL：httpsXXXjapanese.engadget.comYYY
  - 使用不可の文字（％など）をXXX,YYYに置き換えている

- 以下をChromeのURL欄に入力する
```
/api/httpsXXXjapanese.engadget.comYYY
```

## ブログ記事をブックマークしているユーザーをクローリング
- このようなページのブックマーク者のリストをクローリングする　http://b.hatena.ne.jp/entry/s/japanese.engadget.com/2019/04/01/ipod/
- サンプルURL：httpXXXb.hatena.ne.jpYYYentryYYYsYYYjapanese.engadget.comYYY2019YYY04YYY01YYYipodYYY
  - 使用不可の文字（％,/,:(コロン)// など）をXXX,YYY,Zに置き換えている

- 以下をChromeのURL欄に入力する
  ```
  /api/bookmark/httpXXXb.hatena.ne.jpYYYentryYYYsYYYjapanese.engadget.comYYY2019YYY04YYY01YYYipodYYY
  ```
