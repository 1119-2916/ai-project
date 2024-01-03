# discord にセルフホストした LLM と会話出来る bot を爆誕させたい

## 動作環境
python 3.12
poetry 1.7

# Makefile 解説
## requirements:
poetry で requirements を吐き出す

## install:
poetry で .venv を生成する

## run:
discord bot を実行する

## generate_dataset:
train_data_generator を実行する。plane text などから学習用のフォーマットにしたファイルを吐き出す

## validate_format:
公式から提供されている学習用 jsonl のバリデータ。トークン数も分かる

## upload:
open ai に jsonl をアップロードする

## tuning:
open ai にアップロードした jsonl を元に、ファインチューニングを実行する
