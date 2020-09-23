import json
import os
import cv2

with open("data/0021500105.json", "r") as f:
    raw_data = json.load(f)

for key_1, value_1 in raw_data.items():
    
