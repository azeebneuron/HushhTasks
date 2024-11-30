# download_model.py
import os
import requests
from tqdm import tqdm
import sys

def download_with_progress(url: str, destination: str):
    """Download file with progress bar and size verification"""
    try:
        EXPECTED_SIZE_GB = 3.80  # Correct expected size
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        print(f"Starting download of {EXPECTED_SIZE_GB:.2f} GB...")
        
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        progress = tqdm(
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        )
        
        with open(destination, 'wb') as file:
            for data in response.iter_content(chunk_size=1024*1024):  # 1MB chunks
                size = file.write(data)
                progress.update(size)
        
        progress.close()
        
        # Verify file size after download
        actual_size = os.path.getsize(destination)
        actual_size_gb = actual_size / (1024*1024*1024)
        
        # Allow for small variations in size (±0.1 GB)
        if abs(actual_size_gb - EXPECTED_SIZE_GB) > 0.1:
            print(f"Warning: Downloaded file size ({actual_size_gb:.2f} GB) differs from expected size ({EXPECTED_SIZE_GB:.2f} GB)")
            return False
            
        print(f"\nDownload completed! File size: {actual_size_gb:.2f} GB")
        return True
        
    except Exception as e:
        print(f"Error during download: {str(e)}")
        return False

def main():
    MODEL_URL = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
    MODEL_PATH = "models/llama/llama-2-7b-chat.Q4_K_M.gguf"
    
    print("Starting LLaMA model download...")
    
    if os.path.exists(MODEL_PATH):
        print(f"Removing existing incomplete file at {MODEL_PATH}")
        os.remove(MODEL_PATH)
    
    success = download_with_progress(MODEL_URL, MODEL_PATH)
    
    if success:
        # Verify final file size
        size_gb = os.path.getsize(MODEL_PATH) / (1024*1024*1024)
        if abs(size_gb - 3.80) > 0.1:  # Allow ±0.1 GB variation
            print(f"Error: Downloaded file size ({size_gb:.2f} GB) is incorrect")
            os.remove(MODEL_PATH)
            return False
            
        print("Download and verification successful!")
        return True
    else:
        print("Download failed!")
        if os.path.exists(MODEL_PATH):
            os.remove(MODEL_PATH)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)