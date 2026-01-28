import google.generativeai as genai
import os

# Ganti dengan API KEY kamu
genai.configure(api_key="AIzaSyCZQ6GsE-i3uvg676kDrrazra75ZNuV4-k")

print("Mencari model yang tersedia...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")