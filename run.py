import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import requests

# ====================
# Fungsi-fungsi utama
# ====================
def web_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1200")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    return driver

def extract_page_number(text):
    """Ekstrak angka dari teks seperti '96 pages' → 96"""
    try:
        return int(text.strip().split()[0])
    except Exception as e:
        st.warning(f"Gagal mengekstrak jumlah halaman: {e}")
        return 0

def download_image_safe(url, file_path, retries=3, delay=2):
    for attempt in range(retries):
        try:
            if url and url.startswith("http"):
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(r.content)
                    return True
                else:
                    st.warning(f"[{attempt+1}] Non-200 response: {r.status_code}")
            else:
                st.error(f"Invalid URL: {url}")
                break
        except Exception as e:
            st.warning(f"[{attempt+1}] Failed to download {url}: {e}")
            time.sleep(delay)
    return False

def download_images_from_gallery(driver, gallery_url, total_pages, folder_prefix="downloaded"):
    try:
        driver.get(gallery_url)
        time.sleep(2)

        first_img = driver.find_element(By.XPATH, "//div[@id='gdt']//a[1]")
        first_img.click()
        time.sleep(2)

        folder_name = f"downloads/{folder_prefix}"
        os.makedirs(folder_name, exist_ok=True)

        for img_index in range(total_pages):
            try:
                image = driver.find_element(By.CSS_SELECTOR, '#img')
                image_url = image.get_attribute('src')
                file_name = os.path.join(folder_name, f"{folder_prefix}_{img_index}.jpg")

                st.write(f"Downloading image {img_index + 1}: {image_url}")
                success = download_image_safe(image_url, file_name)

                if success:
                    st.success(f"Saved as {file_name}")
                else:
                    st.error(f"Failed to download image {img_index + 1}, skipping...")

                next_button = driver.find_element(By.ID, 'next')
                next_button.click()
                time.sleep(2)
            except Exception as e:
                st.error(f"Error at image {img_index + 1}: {e}")
                continue
    finally:
        driver.quit()
        st.info("Scraping finished.")

# ========================
# STREAMLIT APP START HERE
# ========================
st.title("📸 E-Hentai Downloader")

gallery_url = st.text_input("Masukkan URL Galeri", placeholder="https://e-hentai.org/g/...")
folder_prefix = st.text_input("Nama Folder Simpan", value="downloaded_gallery")

# Tombol Cek halaman (opsional untuk debugging)
#if st.button("Cek halaman"):
    #if not gallery_url.strip():
        #st.warning("Silakan masukkan URL galeri terlebih dahulu.")
    #else:
        #driver = web_driver()
        #try:
            #driver.get(gallery_url)
            #wait = WebDriverWait(driver, 10)
            #pages = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='gdd']/table/tbody/tr[6]/td[2]")))
            #full_text = pages.text
            #page_number = extract_page_number(full_text)

            #st.success("Data berhasil diambil!")
            #st.write("Isi elemen:", full_text)
            #st.write("Jumlah halaman (angka):", page_number)
        #except Exception as e:
            #st.error(f"Gagal mengambil data: {e}")
        #finally:
            #driver.quit()

# Tombol Download (otomatis hitung jumlah halaman)
if st.button("Download"):
    if not gallery_url.strip():
        st.warning("Silakan masukkan URL galeri terlebih dahulu.")
    else:
        st.info("Mengambil jumlah halaman...")
        driver = web_driver()
        try:
            driver.get(gallery_url)
            wait = WebDriverWait(driver, 10)
            pages = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='gdd']/table/tbody/tr[6]/td[2]")))
            full_text = pages.text
            total_pages = extract_page_number(full_text)

            if total_pages > 0:
                st.success(f"Jumlah halaman: {total_pages}")
                st.info("Memulai proses scraping...")
                download_images_from_gallery(driver, gallery_url.strip(), total_pages, folder_prefix)
            else:
                st.error("Gagal mendeteksi jumlah halaman.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat mengambil jumlah halaman: {e}")
            driver.quit()
