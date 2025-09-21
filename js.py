from bs4 import BeautifulSoup
import requests
import argparse
import re
import json
import threading
from urllib.parse import urljoin

def load_patterns(path="patterns.txt"):
    patterns = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for ln in f:
                ln = ln.strip()
                if not ln or ln.startswith('#'):
                    continue
                if ':' in ln:
                    name, rx = ln.split(':', 1)
                else:
                    name, rx = ln, ln
                try:
                    patterns.append((name.strip(), re.compile(rx)))
                except re.error:
                    print(f"[BAD PATTERN] {ln}")
    except FileNotFoundError:
        print(f"[WARN] pattern file not found: {path}")
    return patterns

def scan_js_for_patterns(js_url, patterns, report_out="report.jsonl"):
    try:
        r = requests.get(js_url, timeout=10)
    except requests.RequestException:
        return
    if r.status_code != 200:
        return
    text = r.text
    findings = []
    for name, pat in patterns:
        for m in pat.finditer(text):
            snippet = m.group(0)
            findings.append({"type": name, "url": js_url, "match": snippet[:200]})
            print("[FIND]" + f" {name} -> {js_url} -> {snippet[:80]}")
    if findings:
        with open(report_out, 'a', encoding='utf-8') as fo:
            for f in findings:
                fo.write(json.dumps(f) + "\n")


def js_out(url,output):
    with open(output,'a') as f:
        f.write(url+"\n")


def extract_urls(url,output):    
    try:
            res = requests.get(url,timeout=5)
            if res.status_code == 200:
                soap = BeautifulSoup(res.text,'html.parser')

            for arg in soap.find_all("a"):
                js_url = arg.get("href")
                if js_url and re.search(r"\.js$",js_url):
                    full_url = urljoin(url,js_url)
                    print("[JS]" + f" {full_url}")
                    js_out(full_url,output)

            for arg in soap.find_all("script"):
                js_url = arg.get("src")
                if js_url and re.search(r"\.js$",js_url):
                    full_url = urljoin(url,js_url)
                    print("[JS]" + f" {full_url}")
                    js_out(full_url,output)
                    
                    patterns = load_patterns("patterns.txt")  # optional: move this outside the loop for efficiency
                    if patterns:
                        scan_js_for_patterns(full_url, patterns, "report.jsonl")
    except Exception:
        print(f"[ERROR] {url}")
        

def banner():
    print('''
   ◣　　　◢
　　█◣　◢█
　　█████       
　　▉┃▉┃█       
　　█████　 ◢◤
　　◥████　 █   Author : zeropwned
　　　████◣ ◥◣  Finding Hidden Secrets :)
　　　█████◣ █
　　　██████ █
　　　██████ █
　　　██████◢█
　　　███████◤
　　　◥█████◤       

    ''')

def main():
    try:
        parser = argparse.ArgumentParser(description="Deep Analyze for credentials in JS files.")
        banner()
        parser.add_argument("--url","-u",help="Url to parse js links.")
        parser.add_argument("--sub","-s",help="Path to enter subdomains")
        parser.add_argument("--output","-o",help="Path to save output.")
        args = parser.parse_args()
        
        if args.url == "" and args.sub == "":
            return
        if not args.output:
            args.output = "js.txt"
        if args.url:
            extract_urls(args.url,args.output)
        
        if args.sub:
            threads = []
            with open(args.sub,'r') as f:
                for subs in f:
                    subs = subs.strip()
                    if not subs:
                        continue
                    for scheme in ("https://","http://"):
                        url = scheme + subs
                        try:
                            t = threading.Thread(target=extract_urls,args=(url,args.output))
                            threads.append(t)
                            t.start()
                        except Exception:
                            print(f"[ERROR] Could not fetch {url}")
            for t in threads:
                t.join()
    except KeyboardInterrupt:
        print(f"\nBye Bye :)")
    
if __name__ == '__main__':
    main()