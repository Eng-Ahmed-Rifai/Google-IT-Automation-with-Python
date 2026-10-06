#!/usr/bin/env python3
"""
Comprehensive Assertion Test Suite for Course 2 Modules
Google IT Automation with Python - Using Python to Interact with the Operating System
"""

import os
import tempfile
import unittest

from module1_health_check import check_disk_usage, check_cpu_usage, system_health_status
from module2_files_and_directories import create_sample_csv, read_csv_data, get_file_metadata, find_files_by_extension
from module3_regular_expressions import extract_pid, validate_web_address, transform_record, replace_domain
from module4_log_processing import filter_log_by_pattern, count_usernames_in_logs
from module5_unit_testing import load_email_directory, find_email, safe_divide
from module6_file_rename_substitute import generate_rename_pairs, batch_rename_files
from module7_log_analysis_final_project import (
    parse_syslog,
    sort_errors_by_frequency,
    sort_users_alphabetically,
    export_errors_to_csv,
    export_users_to_csv,
    convert_csv_to_html
)


class TestCourse2Suite(unittest.TestCase):

    def test_module1_health_check(self):
        status = system_health_status()
        self.assertIn("disk_healthy", status)
        self.assertIn("cpu_healthy", status)
        self.assertIn("all_healthy", status)
        self.assertTrue(check_disk_usage("/", 0.01))

    def test_module2_files_and_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            data = [{"name": "Ahmed", "role": "Engineer"}, {"name": "Sara", "role": "Data Analyst"}]
            create_sample_csv(csv_path, data)
            read_back = read_csv_data(csv_path)
            self.assertEqual(len(read_back), 2)
            self.assertEqual(read_back[0]["name"], "Ahmed")

            meta = get_file_metadata(csv_path)
            self.assertTrue(meta["is_file"])
            self.assertGreater(meta["size_bytes"], 0)

            found = find_files_by_extension(tmpdir, ".csv")
            self.assertEqual(len(found), 1)

    def test_module3_regex(self):
        pid = extract_pid("July 31 07:51:48 mycomputer bad_process[12345]: ERROR")
        self.assertEqual(pid, "12345")
        self.assertIsNone(extract_pid("No pid here"))

        self.assertTrue(validate_web_address("https://www.coursera.org/learn/python"))
        self.assertFalse(validate_web_address("not a url"))

        trans = transform_record("Rifai, Ahmed, 555-123-4567")
        self.assertEqual(trans, "Ahmed Rifai: +1-555-123-4567")

        replaced = replace_domain("ahmed@mycompany.com", "mycompany.com", "google.com")
        self.assertEqual(replaced, "ahmed@google.com")

    def test_module4_log_processing(self):
        sample_logs = [
            "May 27 11:45:40 CRON[10844]: (root) CMD (test)",
            "May 27 11:45:41 systemd[1]: USER (ahmed) logged in",
            "May 27 11:45:42 systemd[1]: USER (ahmed) session started",
            "May 27 11:45:43 systemd[1]: USER (jane) logged in",
        ]
        cron_lines = filter_log_by_pattern(sample_logs, r"CRON")
        self.assertEqual(len(cron_lines), 1)

        counts = count_usernames_in_logs(sample_logs)
        self.assertEqual(counts.get("ahmed"), 2)
        self.assertEqual(counts.get("jane"), 1)

    def test_module5_unit_testing(self):
        email_dict = {"ahmed rifai": "ahmed@example.com", "jane doe": "jane@example.com"}
        self.assertEqual(find_email(email_dict, "Ahmed Rifai"), "ahmed@example.com")
        self.assertEqual(find_email(email_dict, "Jane Doe"), "jane@example.com")
        self.assertEqual(find_email(email_dict, "Non Existent"), "No email address found")
        self.assertEqual(find_email(email_dict, None), "Missing parameters")
        self.assertEqual(find_email(email_dict, ""), "Missing parameters")

        self.assertEqual(safe_divide(10, 2), 5.0)
        self.assertIsNone(safe_divide(10, 0))

    def test_module6_substring_rename(self):
        files = ["/data/jane_report.txt", "/data/jane_summary.csv", "/data/john_notes.txt"]
        pairs = generate_rename_pairs(files, "jane", "jdoe")
        self.assertEqual(len(pairs), 2)
        self.assertEqual(pairs[0], ("/data/jane_report.txt", "/data/jdoe_report.txt"))

        count = batch_rename_files(pairs, dry_run=True)
        self.assertEqual(count, 2)

    def test_module7_log_analysis_final_project(self):
        lines = [
            "Jan 31 00:09:39 ubuntu.local ticky: INFO Created ticket [#1234] (ahmed.r)",
            "Jan 31 00:16:53 ubuntu.local ticky: ERROR The ticket was modified while updating (ahmed.r)",
            "Jan 31 00:21:30 ubuntu.local ticky: ERROR Permission denied while closing ticket (sara.d)",
            "Jan 31 00:22:00 ubuntu.local ticky: ERROR Permission denied while closing ticket (ahmed.r)",
            "Jan 31 00:23:00 ubuntu.local ticky: INFO Closed ticket [#1234] (sara.d)",
        ]
        errors, users = parse_syslog(lines)

        self.assertEqual(errors["Permission denied while closing ticket"], 2)
        self.assertEqual(errors["The ticket was modified while updating"], 1)
        self.assertEqual(users["ahmed.r"]["INFO"], 1)
        self.assertEqual(users["ahmed.r"]["ERROR"], 2)
        self.assertEqual(users["sara.d"]["INFO"], 1)
        self.assertEqual(users["sara.d"]["ERROR"], 1)

        sorted_err = sort_errors_by_frequency(errors)
        self.assertEqual(sorted_err[0][0], "Permission denied while closing ticket")
        self.assertEqual(sorted_err[0][1], 2)

        sorted_usr = sort_users_alphabetically(users)
        self.assertEqual(sorted_usr[0][0], "ahmed.r")
        self.assertEqual(sorted_usr[1][0], "sara.d")

        with tempfile.TemporaryDirectory() as tmpdir:
            err_csv = os.path.join(tmpdir, "error_message.csv")
            usr_csv = os.path.join(tmpdir, "user_statistics.csv")
            export_errors_to_csv(sorted_err, err_csv)
            export_users_to_csv(sorted_usr, usr_csv)

            self.assertTrue(os.path.exists(err_csv))
            self.assertTrue(os.path.exists(usr_csv))

            html = convert_csv_to_html(err_csv)
            self.assertIn("<table>", html)
            self.assertIn("<th>Error</th>", html)
            self.assertIn("<th>Count</th>", html)


if __name__ == "__main__":
    unittest.main()
