import os, time, requests, shutil, hashlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def download_from_threads(username):
    folder = f"downloads/{username}"
    os.makedirs(folder, exist_ok=True)
    seen = set()

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.threads.net/@{username}")
    time.sleep(5)

    prev_height = 0
    stable_count = 0
    while stable_count < 8:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        height = driver.execute_script("return document.body.scrollHeight")
        if height == prev_height:
            stable_count += 1
        else:
            stable_count = 0
        prev_height = height

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    count = 0
    for tag in soup.find_all(["img", "source", "video"]):
        src = tag.get("src")
        ext = ".mp4" if (src and ".mp4" in src) else ".jpg"
        if src and "cdn" in src and "profile" not in src:
            h = hashlib.md5(src.encode()).hexdigest()
            if h in seen:
                continue
            seen.add(h)
            r = requests.get(src)
            if r.status_code == 200 and len(r.content) > 30000:
                with open(f"{folder}/media_{count+1}{ext}", "wb") as f:
                    f.write(r.content)
                count += 1

    zip_path = f"{folder}.zip"
    shutil.make_archive(folder, 'zip', folder)
    return zip_path
