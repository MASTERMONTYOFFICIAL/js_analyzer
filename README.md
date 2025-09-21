# 🔍 JS-Secrets-Finder  

![banner](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnR4bHpmaDNqdWVvemV0Y2FrbnJiMzhyNnhqN3ZqdWEzdngxNmNmOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HoffxyN8ghVuw/giphy.gif)  
_Finding hidden secrets inside JavaScript files from websites_  

---

## ⚡ Features
- Extract all `.js` files from target URL or subdomains  
- Scan `.js` files for sensitive patterns (API keys, tokens, credentials)  
- Multi-threading support for fast scanning  
- Saves results in `js.txt` and findings in `report.jsonl`  

---

## 📦 Installation  

```bash
# Clone the repository
https://github.com/MASTERMONTYOFFICIAL/js_analyzer.git
cd js_analyzer
python3 js.py

# Install dependencies
pip3 install requests
pip3 install bs4

# Scan a single URL
python tool.py -u https://example.com -o output.txt

# Scan using subdomains file
python tool.py -s subs.txt -o output.txt

```
[!Click Here](https://youtu.be/F4fEC9W7Uo8)(https://youtu.be/F4fEC9W7Uo8)]

