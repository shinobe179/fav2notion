fav2notion
----------

いいねしたツイートをNotionのデータベースへ送信します。AWS Lambdaで動きます。

## 使い方

- Twitterでやること
    - Twitter Appを登録して、API key, API secret, Access token, Access token secretを取得しておきます。
- Notionでやること
    - My integrationを作ってAPIトークンを取得します。
        - pageをretrieve, insert, updateする権限が必要です。
    - ツイート記録用データベースと、ポインタ記録用ページを作ります。
    - ツイート記録用データベースと、ポインタ記録用ページそれぞれでMy integrationをconnectします。
    - いいねしたツイートの保存は、最近いいねしたものから遡って行われます。初回実行時に保存したいツイートのうち、最も古いツイートのツイートIDを、ポインタ記録用ページに（H1やH2ではなく、テキストで）記録しておきます。
- AWSでやること
    - このリポジトリをクローンしてきて `make` すると、lambda_packages.zipというファイルが生成されます。
    - ランタイムとしてPython3.9を使うAWS Lambda関数を作って、lambda_packages.zipをアップロードしてください。
    - おびただしい数の環境変数が必要です。根気よく設定してください。
        - `TWITTER_API_KEY`
        - `TWITTER_API_KEY_SECRET`
        - `TWITTER_ACCESS_TOKEN`
        - `TWITTER_ACCESS_TOKEN_SECRET`
        - `TWITTER_USER_ID`
            - TwitterのユーザーID
        - `NOTION_API_TOKEN`
            - NotionのAPIトークン
        - `NOTION_POINTER_PAGE_ID`
            - ポインターを記録しておくNotionページのID
        - `NOTION_PARENT_DATABASE_ID`
            - ツイートを記録するNotionデータベースのID
    - Lambda関数の実行時間を適当に設定してください。
    - EventBridge Schedulerで任意の時間間隔で実行するよう設定してください。

## 仕組み

- Notionのポインタ記録用ページからポインタを取得します。
    - ポインタとは、前回実行時に最近いいねしたツイートのIDです。
- `Tweepy.Client.get_liked_tweets()` で、自分がいいねしたツイートのリストを取得します。
    - ツイートの取得数は30件、ページングの実装をしていないので、たくさんいいねする方は以下をご検討ください。
        - twitter.pyを修正する
            - ツイートの取得数を増やす
            - ページングを実装する
        - EventBridge Schedulerで実行間隔を短くする
    - 30件としているのは、Twitter API v2のEssential accessだと月50万件までツイートを取得でき、5分間隔で実行するとこれに十分収まる見込みだからです。
        - `30件 * 12回 * 24時間 * 30日 = 259,200件`
- リストの先頭のツイート（最近いいねしたツイート）のIDを、次回実行時のポインタとして変数に保存します。
- リストを先頭から列挙していき、Notionデータベースへ保存します。これを、ツイートIDがポインタと合致するまでループします。
- ツイートIDがポインタと合致するツイートまで来たら、ループ処理から抜けます。
- Notionのポインタ用ページの内容を、今回保存しておいたポインタに更新します。

## ToDo

- Serverless Architecture Modelでデプロイをしやすくする
    - でも `sam` のインストールを案内しなきゃならないの面倒
- loggerの実装
- Python3.10で作っちゃったけど、Lambdaのランタイムは3.9までしかなかった
