from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Chrome tidak langsung tertutup otomatis
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Skenario Test Format (ID, Username, Password, Jenis, Pesan_Error_Diharapkan)
test_scenarios = [
    # TEST CASE POSITIF 
    ("TP01", "standard_user", "secret_sauce", "Positif", None),
    ("TP02", "problem_user", "secret_sauce", "Positif", None),
    ("TP03", "performance_glitch_user", "secret_sauce", "Positif", None),
    ("TP04", "error_user", "secret_sauce", "Positif", None),
    ("TP05", "visual_user", "secret_sauce", "Positif", None),

    # TEST CASE NEGATIF
    ("TN01", "standard_user", "salah_password", "Negatif", "Username and password do not match"),
    ("TN02", "user_gaib", "secret_sauce", "Negatif", "Username and password do not match"),
    ("TN03", "", "secret_sauce", "Negatif", "Username is required"),
    ("TN04", "standard_user", "", "Negatif", "Password is required"),
    ("TN05", "locked_out_user", "secret_sauce", "Negatif", "Sorry, this user has been locked out")
]

def run_test():
    print("=== MEMULAI AUTOMATION TEST SUITE ===\n")
    
    for id_tc, user, pw, jenis, expected_err in test_scenarios:
        print(f"Running {id_tc}: {jenis} - User: '{user}'")
        
        driver.get("https://www.saucedemo.com/")
        
        driver.find_element(By.ID, "user-name").clear()
        driver.find_element(By.ID, "user-name").send_keys(user)
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(pw)
        driver.find_element(By.ID, "login-button").click()
        
        time.sleep(1) 
        
        if "inventory.html" in driver.current_url:
            print(f"   RESULT: ✅ PASS (Login Berhasil)")
            
            # Logout agar bisa lanjut ke test case berikutnya
            driver.get("https://www.saucedemo.com/") 
        else:
            try:
                error_msg = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
                if expected_err and expected_err.lower() in error_msg.lower():
                    print(f"   RESULT: ✅ PASS (Error Sesuai: '{error_msg}')")
                else:
                    print(f"   RESULT: ❌ FAIL (Pesan Error Berbeda: '{error_msg}')")
            except:
                print("   RESULT: ❌ FAIL (Login Gagal tapi pesan error tidak ditemukan)")
        
        print("-" * 50)

try:
    run_test()
finally:
    print("\nSemua tes selesai dijalankan.")
    input("Tekan Enter untuk menutup browser...")
    driver.quit()