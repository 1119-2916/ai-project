from openai import OpenAI
from private.secrets import OPENAI_API_SECRET, TRAIN_DATA_FILE_ID, TRAIN_DATA_FILE_PATH
import sys


client = OpenAI(api_key=OPENAI_API_SECRET)


def upload_training_data(key:str):
    train_data_path = TRAIN_DATA_FILE_PATH[key]
    client.files.create(file=open(train_data_path, "rb"), purpose="fine-tune")


def create_fine_tuning_job(key:str):
    file_id = TRAIN_DATA_FILE_ID[key]
    client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-3.5-turbo"
    )


def main():
    args = sys.argv
    if len(args) < 2:
        print("invalid argument")
        return
    if args[1] == "upload":
        upload_training_data(args[2])
    elif args[1] == "tuning":
        create_fine_tuning_job(args[2])
    else:
        print("invalid argument")

if __name__ == "__main__":
    main()
