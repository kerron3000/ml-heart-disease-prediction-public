import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestHeartIQ:
    @pytest.fixture(scope="class")
    def driver(self):
        # Setup: Ensure the Streamlit app is running via Docker or locally
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless") # Uncomment for CI/CD pipelines
        driver = webdriver.Chrome(options=options)
        driver.get("http://localhost:8501")
        yield driver
        # Teardown
        driver.quit()

    def test_page_title(self, driver):
        """Verify the app loads with the correct header."""
        wait = WebDriverWait(driver, 10)
        title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        assert "Heart Disease Prediction Tool" in title.text

    def test_input_fields_presence(self, driver):
        """Check if both Numerical and Categorical columns are rendered."""
        # Streamlit renders subheaders as h3 by default
        subheaders = driver.find_elements(By.TAG_NAME, "h3")
        texts = [s.text for s in subheaders]
        assert "Numerical Inputs" in texts
        assert "Categorical Inputs" in texts

    def test_prediction_flow(self, driver):
        """Simulate a user clicking the predict button and seeing a result."""
        # 1. Wait for the 'Predict Diagnosis' button
        # Streamlit buttons are often identifiable by the text inside a <button> tag
        predict_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Predict Diagnosis')]"))
        )
        
        # 2. Click the button (using default slider values)
        predict_button.click()

        # 3. Wait for the result to appear
        # The app displays results in an 'st.error' or 'st.success' block
        result_header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Prediction:')]"))
        )
        
        assert "Prediction:" in result_header.text
        
        # 4. Check for Confidence Level text
        confidence = driver.find_element(By.XPATH, "//*[contains(text(), 'Confidence Level')]")
        assert confidence.is_displayed()
