#!/usr/bin/env python3
"""
Comprehensive Assertion Test Suite for Course 3 Modules
Google IT Automation with Python - Introduction to Git and GitHub
"""

import unittest

from module1_git_basics import parse_git_status_porcelain
from module2_branching_and_merging import detect_conflict_markers, resolve_conflict_favoring_incoming
from module3_remotes_and_github import parse_github_url, build_authenticated_url
from module4_pull_requests_and_collaboration import format_commit_message, generate_pr_summary


class TestCourse3Suite(unittest.TestCase):

    def test_module1_status_parser(self):
        sample_porcelain = (
            "M  file1.py\n"
            " M file2.txt\n"
            "?? untracked.py\n"
        )
        parsed = parse_git_status_porcelain(sample_porcelain)
        self.assertIn("file1.py", parsed["staged"])
        self.assertIn("file2.txt", parsed["unstaged"])
        self.assertIn("untracked.py", parsed["untracked"])

    def test_module2_merge_conflicts(self):
        conflict_text = (
            "def greet():\n"
            "<<<<<<< HEAD\n"
            "    print('Hello World')\n"
            "=======\n"
            "    print('Hello Git!')\n"
            ">>>>>>> feature-branch\n"
        )
        conflicts = detect_conflict_markers(conflict_text)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["current_branch"], "HEAD")
        self.assertEqual(conflicts[0]["incoming_branch"], "feature-branch")
        self.assertEqual(conflicts[0]["incoming_code"], "print('Hello Git!')")

        resolved = resolve_conflict_favoring_incoming(conflict_text)
        self.assertNotIn("<<<<<<<", resolved)
        self.assertNotIn("=======", resolved)
        self.assertNotIn(">>>>>>>", resolved)
        self.assertIn("print('Hello Git!')", resolved)

    def test_module3_remotes_and_urls(self):
        https_url = "https://github.com/Eng-Ahmed-Rifai/Google-IT-Automation-with-Python.git"
        parsed_https = parse_github_url(https_url)
        self.assertIsNotNone(parsed_https)
        self.assertEqual(parsed_https["owner"], "Eng-Ahmed-Rifai")
        self.assertEqual(parsed_https["repo"], "Google-IT-Automation-with-Python")
        self.assertEqual(parsed_https["protocol"], "https")

        ssh_url = "git@github.com:Eng-Ahmed-Rifai/Google-IT-Automation-with-Python.git"
        parsed_ssh = parse_github_url(ssh_url)
        self.assertIsNotNone(parsed_ssh)
        self.assertEqual(parsed_ssh["protocol"], "ssh")

        auth_url = build_authenticated_url(parsed_https, "ahmed", "ghp_secrettoken")
        self.assertTrue(auth_url.startswith("https://ahmed:ghp_secrettoken@github.com/"))

    def test_module4_collaboration_and_pr(self):
        msg = format_commit_message("feat: add git automation module", "Adds robust helpers for status and diffs.", 101)
        self.assertIn("feat: add git automation module", msg)
        self.assertIn("Closes #101", msg)

        pr = generate_pr_summary(
            title="Add Branching and Merge Resolvers",
            feature_desc="Adds automated resolution routines for 3-way conflicts.",
            changes=["Added regex marker parsing", "Added incoming changes resolution helper"],
            tested=True
        )
        self.assertTrue(pr["ready_to_merge"])
        self.assertIn("## Description", pr["body"])
        self.assertIn("- [x] All automated tests pass", pr["body"])


if __name__ == "__main__":
    unittest.main()
