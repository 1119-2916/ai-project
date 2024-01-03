from openai import OpenAI
from private.secrets import OPENAI_API_SECRET, TRAIN_DATA_FILE_ID
import sys


client = OpenAI(api_key=OPENAI_API_SECRET)


def upload_training_data():
    # discord のほう
    # train_data_path = "./train_data/train_data.jsonl"
    # twitter のほう
    train_data_path = "./train_data/twitter_11192916.jsonl"
    client.files.create(file=open(train_data_path, "rb"), purpose="fine-tune")


def create_fine_tuning_job():
    file_id = TRAIN_DATA_FILE_ID
    client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-3.5-turbo"
    )


def main():
    args = sys.argv
    if args[1] == "upload":
        upload_training_data()
    elif args[1] == "tuning":
        create_fine_tuning_job()
    else:
        print("invalid argument")

if __name__ == "__main__":
    main()
