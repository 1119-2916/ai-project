# twitter から学習用データを抽出するやつ

1. ツイッターから過去ツイートを全部ダウンロードしてくる
2. tweets.js のみをここにコピーしてくる
3. `python extractor.py` で tweets.js からツイートのみ抽出して、バリデーションとクレンズをする
4. output.txt が生成される。1行に1つ学習データがある。
5. 1個ディレクトリ戻って `make generate_dataset` する
