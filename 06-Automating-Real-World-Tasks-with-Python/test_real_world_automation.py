"""
Google IT Automation with Python - Course 6: Automating Real-World Tasks with Python
Comprehensive Test Suite (test_real_world_automation.py)

Validates all Course 6 modules with 100.00% precision:
- TestModule1ImageProcessing
- TestModule2WebServices
- TestModule3EmailPDF
- TestModule4CatalogAutomation
- TestHealthCheck
"""

import os
import shutil
import socket
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from PIL import Image
import requests

import module1_image_processing as m1
import module2_web_services as m2
import module3_email_pdf as m3
import module4_catalog_automation as m4
import health_check as hc


class TestModule1ImageProcessing(unittest.TestCase):
    """Validation tests for Module 1: Image Processing with Pillow"""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_process_single_image(self):
        input_img = os.path.join(self.tmp_dir, "sample.png")
        output_img = os.path.join(self.tmp_dir, "processed.jpg")

        # Create RGBA test image (300x200)
        im = Image.new("RGBA", (300, 200), (255, 128, 0, 200))
        im.save(input_img)

        # Process image: resize to 128x128, rotate 90 clockwise
        ok = m1.process_single_image(
            input_path=input_img,
            output_path=output_img,
            target_size=(128, 128),
            rotate_clockwise_degrees=90,
            target_format="JPEG"
        )
        self.assertTrue(ok)
        self.assertTrue(os.path.exists(output_img))

        with Image.open(output_img) as result_im:
            self.assertEqual(result_im.size, (128, 128))
            self.assertEqual(result_im.format, "JPEG")
            self.assertEqual(result_im.mode, "RGB")

    def test_batch_process_images(self):
        in_dir = os.path.join(self.tmp_dir, "inputs")
        out_dir = os.path.join(self.tmp_dir, "outputs")
        os.makedirs(in_dir, exist_ok=True)

        for i in range(3):
            im_path = os.path.join(in_dir, f"img_{i}.tiff")
            Image.new("RGB", (100, 100), (i * 50, 100, 200)).save(im_path, "TIFF")

        processed = m1.batch_process_images(in_dir, out_dir, target_size=(128, 128))
        self.assertEqual(len(processed), 3)
        for p in processed:
            self.assertTrue(os.path.exists(p))


class TestModule2WebServices(unittest.TestCase):
    """Validation tests for Module 2: Web Services & REST APIs"""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_parse_feedback_file(self):
        f_path = os.path.join(self.tmp_dir, "feedback_1.txt")
        with open(f_path, "w", encoding="utf-8") as f:
            f.write("Fast Delivery\n")
            f.write("Sarah Conner\n")
            f.write("2026-10-08\n")
            f.write("Received the hardware package within 24 hours.\n")
            f.write("Great service!\n")

        res = m2.parse_feedback_file(f_path)
        self.assertEqual(res["title"], "Fast Delivery")
        self.assertEqual(res["name"], "Sarah Conner")
        self.assertEqual(res["date"], "2026-10-08")
        self.assertIn("Received the hardware package", res["feedback"])
        self.assertIn("Great service!", res["feedback"])

    def test_post_feedback_to_api_success(self):
        data = {"title": "Test", "name": "Tester", "date": "2026-10-08", "feedback": "Nice"}
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.text = '{"success": true}'

        with patch("requests.post", return_value=mock_resp):
            ok, status, text = m2.post_feedback_to_api("http://api.internal/feedback", data)
            self.assertTrue(ok)
            self.assertEqual(status, 201)

    def test_post_feedback_to_api_retries_on_500(self):
        data = {"title": "Retry Test", "name": "Tester", "date": "2026-10-08", "feedback": "Retry"}
        mock_500 = MagicMock()
        mock_500.status_code = 500
        mock_500.text = "Internal Server Error"

        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.text = "OK"

        # Simulates 500 on first try, 200 on second try
        with patch("requests.post", side_effect=[mock_500, mock_200]):
            ok, status, _ = m2.post_feedback_to_api(
                "http://api.internal/feedback",
                data,
                max_retries=3,
                backoff_factor=0.01
            )
            self.assertTrue(ok)
            self.assertEqual(status, 200)


class TestModule3EmailPDF(unittest.TestCase):
    """Validation tests for Module 3: PDF Generation & Email Dispatch"""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_process_car_sales_data(self):
        dataset = [
            {"id": 1, "car": {"car_make": "Honda", "car_model": "Civic", "car_year": 2015}, "price": "$12,000.00", "total_sales": 80},
            {"id": 2, "car": {"car_make": "Ford", "car_model": "F-150", "car_year": 2018}, "price": "$30,000.00", "total_sales": 50},
            {"id": 3, "car": {"car_make": "Honda", "car_model": "Accord", "car_year": 2018}, "price": "$15,000.00", "total_sales": 60},
        ]
        # Revenue:
        # Honda Civic: 12000 * 80 = 960,000
        # Ford F-150: 30000 * 50 = 1,500,000 (Max revenue)
        # Honda Accord: 15000 * 60 = 900,000
        # Sales: Honda Civic = 80 (Max sales)
        # Year 2018 total sales: 50 + 60 = 110 (Max year)

        table_data, summary = m3.process_car_sales_data(dataset)
        self.assertEqual(len(table_data), 4)
        self.assertIn("Ford F-150 (2018) generated the most revenue: $1,500,000.00", summary[0])
        self.assertIn("Honda Civic (2015) had the most sales: 80", summary[1])
        self.assertIn("The most popular year was 2018 with 110 sales.", summary[2])

    def test_generate_pdf_and_email_with_attachment(self):
        pdf_file = os.path.join(self.tmp_dir, "report.pdf")
        m3.generate_pdf_report(pdf_file, "Sales", "Detailed report", [["A", "B"], ["1", "2"]])
        self.assertTrue(os.path.exists(pdf_file))

        msg = m3.generate_email_message(
            sender="sys@corp.com",
            recipient="admin@corp.com",
            subject="Automated Report",
            body="Here is the PDF.",
            attachment_path=pdf_file
        )
        self.assertEqual(msg["Subject"], "Automated Report")
        attachments = list(msg.iter_attachments())
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0].get_filename(), "report.pdf")

        # Test simulation sending
        self.assertTrue(m3.send_email(msg, simulate=True))


class TestModule4CatalogAutomation(unittest.TestCase):
    """Validation tests for Module 4: Catalog Automation & Supplier Pipeline"""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_process_catalog_image(self):
        raw_img = os.path.join(self.tmp_dir, "005.tiff")
        out_img = os.path.join(self.tmp_dir, "005.jpeg")

        Image.new("RGB", (1200, 800), (10, 20, 30)).save(raw_img, "TIFF")
        ok = m4.process_catalog_image(raw_img, out_img, target_size=(600, 400))
        self.assertTrue(ok)

        with Image.open(out_img) as verified:
            self.assertEqual(verified.size, (600, 400))
            self.assertEqual(verified.format, "JPEG")

    def test_parse_catalog_description(self):
        desc_path = os.path.join(self.tmp_dir, "002.txt")
        with open(desc_path, "w", encoding="utf-8") as f:
            f.write("Banana\n")
            f.write("250 lbs\n")
            f.write("Fresh tropical yellow bananas rich in potassium.\n")

        item = m4.parse_catalog_description(desc_path)
        self.assertEqual(item["name"], "Banana")
        self.assertEqual(item["weight"], 250)
        self.assertIsInstance(item["weight"], int)
        self.assertEqual(item["image_name"], "002.jpeg")
        self.assertIn("Fresh tropical yellow", item["description"])


class TestHealthCheck(unittest.TestCase):
    """Validation tests for Health Check Monitoring"""

    def test_localhost_resolution(self):
        self.assertTrue(hc.check_localhost_resolution("127.0.0.1"))

    def test_health_check_violations_alerting(self):
        with patch("psutil.cpu_percent", return_value=85.0), \
             patch("shutil.disk_usage", return_value=MagicMock(free=10, total=100)), \
             patch("psutil.virtual_memory", return_value=MagicMock(available=100 * 1024 * 1024)), \
             patch("socket.gethostbyname", return_value="10.0.0.1"):

            errors = hc.run_system_health_audit()
            self.assertEqual(len(errors), 4)
            self.assertIn("Error - CPU usage is over 80%", errors)
            self.assertIn("Error - Available disk space is less than 20%", errors)
            self.assertIn("Error - Available memory is less than 500MB", errors)
            self.assertIn("Error - localhost cannot be resolved to 127.0.0.1", errors)

            count = hc.monitor_and_alert(simulate=True)
            self.assertEqual(count, 4)


def run_full_suite() -> int:
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestModule1ImageProcessing))
    suite.addTests(loader.loadTestsFromTestCase(TestModule2WebServices))
    suite.addTests(loader.loadTestsFromTestCase(TestModule3EmailPDF))
    suite.addTests(loader.loadTestsFromTestCase(TestModule4CatalogAutomation))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthCheck))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    import sys
    sys.exit(run_full_suite())
