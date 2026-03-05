from datasets import load_dataset, load_from_disk
import os

DATA_PATH = "data/awesome_chatgpt_prompts"

def download_and_save_dataset():
    # Download dataset from Hugging Face Hub (only happens the first time)
    ds = load_dataset("fka/awesome-chatgpt-prompts")
    
    # Save the dataset locally if not already saved
    if not os.path.exists(DATA_PATH):
        ds.save_to_disk(DATA_PATH)
        print(f"Dataset saved locally at '{DATA_PATH}'")
    else:
        print(f"Dataset already exists at '{DATA_PATH}'")

def load_local_dataset():
    # Load dataset from local disk cache
    ds = load_from_disk(DATA_PATH)
    print("Loaded dataset from local disk:")
    print(ds)
    return ds

if __name__ == "__main__":
    download_and_save_dataset()  # Download and save locally (if not already)
    dataset = load_local_dataset()  # Load from local storage and print info
