import os
import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5003").rstrip("/")
HEADLESS = os.environ.get("HEADLESS", "false").lower() in ("true", "1", "yes")

def wait_for_app(url, timeout=30):
    print(f"[*] Checking application availability at {url}/api/health ...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            res = requests.get(f"{url}/api/health", timeout=2)
            if res.status_code == 200:
                print(f"[+] Application is healthy and ready!")
                return True
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError(f"[-] Application at {url} did not become ready within {timeout} seconds.")

def get_webdriver():
    print(f"[*] Initializing browser driver (headless={HEADLESS})...")
    # Try Edge first (pre-installed on Windows)
    try:
        from selenium.webdriver.edge.options import Options as EdgeOptions
        options = EdgeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,800")
        driver = webdriver.Edge(options=options)
        return driver
    except Exception as e:
        print(f"[*] Edge driver failed: {e}. Trying Chrome...")
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        options = ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,800")
        return webdriver.Chrome(options=options)

def run_tests():
    wait_for_app(BASE_URL)
    driver = get_webdriver()
    wait = WebDriverWait(driver, 10)

    try:
        print(f"\n=======================================================")
        print(f" STARTING SELENIUM TEST SUITE FOR STUDENT MARKS")
        print(f" Target Application URL: {BASE_URL}")
        print(f"=======================================================\n")

        # Test Case 1: Load Page & Verify Elements
        driver.get(BASE_URL)
        time.sleep(1)
        assert "Student Marks Calculation" in driver.title, f"Unexpected page title: {driver.title}"
        wait.until(EC.presence_of_element_located((By.ID, "sub1")))
        wait.until(EC.presence_of_element_located((By.ID, "sub2")))
        wait.until(EC.presence_of_element_located((By.ID, "sub3")))
        wait.until(EC.presence_of_element_located((By.ID, "btn-calculate")))
        print("[PASS] Test 1: Page successfully loaded and all input elements are present.")

        # Test Case 2: Standard Valid Calculation (85, 90, 95)
        # Expected: Total = 270, Avg = 90.0, Grade = A+, Status = Passed
        name_input = driver.find_element(By.ID, "student_name")
        name_input.clear()
        name_input.send_keys("Shruti")

        sub1 = driver.find_element(By.ID, "sub1")
        sub1.clear()
        sub1.send_keys("85")

        sub2 = driver.find_element(By.ID, "sub2")
        sub2.clear()
        sub2.send_keys("90")

        sub3 = driver.find_element(By.ID, "sub3")
        sub3.clear()
        sub3.send_keys("95")

        driver.find_element(By.ID, "btn-calculate").click()
        time.sleep(1.5)

        total_el = wait.until(EC.visibility_of_element_located((By.ID, "total-result")))
        avg_el = wait.until(EC.visibility_of_element_located((By.ID, "average-result")))
        status_el = wait.until(EC.visibility_of_element_located((By.ID, "status-result")))
        grade_el = wait.until(EC.visibility_of_element_located((By.ID, "grade-result")))

        assert "270" in total_el.text, f"Expected 270 in total, got '{total_el.text}'"
        assert "90" in avg_el.text, f"Expected 90 in average, got '{avg_el.text}'"
        assert "passed" in status_el.text.lower(), f"Expected Passed status, got '{status_el.text}'"
        assert "A+" in grade_el.text, f"Expected A+ grade, got '{grade_el.text}'"
        print(f"[PASS] Test 2: Valid marks verified: Total={total_el.text.split()[0]}, Avg={avg_el.text}, Grade={grade_el.text}, Status={status_el.text}")

        # Test Case 3: Second Calculation (70, 75, 80)
        # Expected: Total = 225, Avg = 75.0, Grade = B, Status = Passed
        sub1 = driver.find_element(By.ID, "sub1")
        sub1.clear()
        sub1.send_keys("70")

        sub2 = driver.find_element(By.ID, "sub2")
        sub2.clear()
        sub2.send_keys("75")

        sub3 = driver.find_element(By.ID, "sub3")
        sub3.clear()
        sub3.send_keys("80")

        driver.find_element(By.ID, "btn-calculate").click()
        time.sleep(1.5)

        total_el = wait.until(EC.visibility_of_element_located((By.ID, "total-result")))
        avg_el = wait.until(EC.visibility_of_element_located((By.ID, "average-result")))
        grade_el = wait.until(EC.visibility_of_element_located((By.ID, "grade-result")))

        assert "225" in total_el.text, f"Expected 225 in total, got '{total_el.text}'"
        assert "75" in avg_el.text, f"Expected 75 in average, got '{avg_el.text}'"
        assert "B" in grade_el.text, f"Expected B grade, got '{grade_el.text}'"
        print(f"[PASS] Test 3: Average marks verified: Total={total_el.text.split()[0]}, Avg={avg_el.text}, Grade={grade_el.text}")

        # Test Case 4: Decimal Marks (82.5, 77.5, 80.0)
        # Expected: Total = 240.0, Avg = 80.0
        sub1 = driver.find_element(By.ID, "sub1")
        sub1.clear()
        sub1.send_keys("82.5")

        sub2 = driver.find_element(By.ID, "sub2")
        sub2.clear()
        sub2.send_keys("77.5")

        sub3 = driver.find_element(By.ID, "sub3")
        sub3.clear()
        sub3.send_keys("80.0")

        driver.find_element(By.ID, "btn-calculate").click()
        time.sleep(1.5)

        total_el = wait.until(EC.visibility_of_element_located((By.ID, "total-result")))
        avg_el = wait.until(EC.visibility_of_element_located((By.ID, "average-result")))

        assert "240" in total_el.text, f"Expected 240 in total, got '{total_el.text}'"
        assert "80" in avg_el.text, f"Expected 80 in average, got '{avg_el.text}'"
        print(f"[PASS] Test 4: Decimal marks calculation verified: Total={total_el.text.split()[0]}, Avg={avg_el.text}")

        # Test Case 5: Failing Subject (30, 80, 90) -> Below 35 in sub1
        # Expected: Status = Failed
        sub1 = driver.find_element(By.ID, "sub1")
        sub1.clear()
        sub1.send_keys("30")

        sub2 = driver.find_element(By.ID, "sub2")
        sub2.clear()
        sub2.send_keys("80")

        sub3 = driver.find_element(By.ID, "sub3")
        sub3.clear()
        sub3.send_keys("90")

        driver.find_element(By.ID, "btn-calculate").click()
        time.sleep(1.5)

        status_el = wait.until(EC.visibility_of_element_located((By.ID, "status-result")))
        assert "fail" in status_el.text.lower(), f"Expected Failed status, got '{status_el.text}'"
        print(f"[PASS] Test 5: Failing grade boundary condition verified: Status={status_el.text}")

        # Test Case 6: Reset Functionality
        reset_btn = driver.find_element(By.ID, "btn-reset")
        reset_btn.click()
        time.sleep(1)

        empty_notice = wait.until(EC.presence_of_element_located((By.ID, "empty-state-notice")))
        assert empty_notice.is_displayed()
        print("[PASS] Test 6: Reset button clears results and restores default state.")

        print(f"\n=======================================================")
        print(f" >>> ALL SELENIUM TEST CASES COMPLETED SUCCESSFULLY! <<<")
        print(f"=======================================================\n")
        return True

    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {e}")
        driver.save_screenshot("tests/selenium_error.png")
        print("[*] Screenshot saved to tests/selenium_error.png")
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    success = run_tests()
    if not success:
        sys.exit(1)
