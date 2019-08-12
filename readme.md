# 概要
このプログラムはJCG Shadowverseの登録一覧ページから各種データをスクレイピングするためのツールです。

# 設定方法
ユーザーができる各種設定は全てsetting.pyで可能。<br>
スクレイピングを開始したい登録一覧ページのURLをsetting.pyのURLに入力する。
```python
URL = "https://sv.j-cg.com/compe/view/entrylist/1717"
```
CARD_DATA_OUTPUT_FILE_NAMEとCLASS_DATA_OUTPUT_FILE_NAMEは出力ファイル名を変更したい場合のみ変更する。<br>
デフォルトでは以下のように設定されている。
```python
CARD_DATA_OUTPUT_FILE_NAME = "card_data.csv"
CLASS_DATA_OUTPUT_FILE_NAME = "class_data.csv"
```

# 使用法
main.pyを実行する。

