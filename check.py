import mediapipe
import os

print("\n--- JAANCH SHURU ---")
try:
    print(f"MediaPipe kahan hai: {mediapipe.__file__}")
except:
    print("MediaPipe mil gaya par file path nahi mila (folder ho sakta hai).")

print(f"Current Folder: {os.getcwd()}")
print("--- JAANCH KHATAM ---\n")