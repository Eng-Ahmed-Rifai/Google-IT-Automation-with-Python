"""
Google IT Automation with Python - Course 6: Automating Real-World Tasks with Python
Module 2: Web Services & REST API Integration (module2_web_services.py)

Covers:
- Parsing structured plain-text customer review and feedback files
- Conversion into normalized JSON-compatible Python dictionaries
- Interacting with RESTful Web Services via the `requests` library
- Retry strategies with exponential backoff and error classification
"""

import os
import sys
import time
from typing import Any, Dict, List, Optional
import requests


def parse_feedback_file(file_path: str) -> Dict[str, str]:
    """
    Parses a single feedback file into standard fields:
    - Line 1: title
    - Line 2: name
    - Line 3: date
    - Lines 4+: feedback (joined into single paragraph)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Feedback file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = [line.strip() for line in f.readlines()]

    if len(lines) < 4:
        raise ValueError(
            f"Malformed feedback file '{file_path}': expected at least 4 lines, found {len(lines)}"
        )

    title = lines[0]
    name = lines[1]
    date = lines[2]
    feedback = " ".join([line for line in lines[3:] if line])

    return {
        "title": title,
        "name": name,
        "date": date,
        "feedback": feedback
    }


def parse_feedback_directory(directory_path: str) -> List[Dict[str, str]]:
    """
    Scans directory for .txt feedback files and converts them into a list of dictionaries.
    """
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    feedbacks: List[Dict[str, str]] = []
    for filename in sorted(os.listdir(directory_path)):
        if filename.endswith(".txt") and not filename.startswith("."):
            full_path = os.path.join(directory_path, filename)
            try:
                item = parse_feedback_file(full_path)
                feedbacks.append(item)
            except Exception as exc:
                print(f"[WARNING] Skipping '{filename}': {exc}", file=sys.stderr)

    return feedbacks


def post_feedback_to_api(
    url: str,
    feedback_data: Dict[str, str],
    timeout: float = 5.0,
    max_retries: int = 3,
    backoff_factor: float = 0.5,
    session: Optional[requests.Session] = None
) -> Tuple[bool, int, str]:
    """
    Posts a single feedback dictionary as JSON to REST endpoint.
    Implements retries on transient connection errors or 5xx status codes.
    Returns: (is_success, http_status_code, response_text_or_error)
    """
    requester = session or requests
    attempt = 0

    while attempt < max_retries:
        attempt += 1
        try:
            response = requester.post(url, json=feedback_data, timeout=timeout)
            if response.status_code in (200, 201):
                return True, response.status_code, response.text
            elif response.status_code >= 500:
                # Server-side transient error, retry
                time.sleep(backoff_factor * (2 ** (attempt - 1)))
                continue
            else:
                # Client-side error (4xx), do not retry
                return False, response.status_code, response.text

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as ex:
            if attempt >= max_retries:
                return False, 0, str(ex)
            time.sleep(backoff_factor * (2 ** (attempt - 1)))
        except requests.exceptions.RequestException as ex:
            return False, 0, str(ex)

    return False, 0, "Max retries exceeded"


def batch_post_feedbacks(
    url: str,
    feedbacks: List[Dict[str, str]],
    timeout: float = 5.0
) -> Dict[str, Any]:
    """
    Iterates over list of feedback entries and uploads them sequentially using a shared session.
    """
    results: Dict[str, Any] = {
        "total": len(feedbacks),
        "success_count": 0,
        "failure_count": 0,
        "details": []
    }

    with requests.Session() as session:
        for idx, item in enumerate(feedbacks):
            ok, status, msg = post_feedback_to_api(
                url=url,
                feedback_data=item,
                timeout=timeout,
                session=session
            )
            if ok:
                results["success_count"] += 1
            else:
                results["failure_count"] += 1

            results["details"].append({
                "index": idx,
                "title": item.get("title"),
                "status_code": status,
                "success": ok,
                "message": msg
            })

    return results


def test_module2() -> None:
    """
    Validation assertion test suite for Module 2.
    """
    import tempfile
    from unittest.mock import MagicMock, patch

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create valid test feedback file
        f_path = os.path.join(tmp_dir, "001.txt")
        with open(f_path, "w", encoding="utf-8") as f:
            f.write("Great Experience\n")
            f.write("Ahmed Rifai\n")
            f.write("2026-10-08\n")
            f.write("The automation tools provided excellent productivity gains.\n")
            f.write("Highly recommended for enterprise workflows.\n")

        # Create invalid file (fewer than 4 lines)
        bad_path = os.path.join(tmp_dir, "bad.txt")
        with open(bad_path, "w", encoding="utf-8") as f:
            f.write("Only Title\n")

        # Test single parsing
        parsed = parse_feedback_file(f_path)
        assert parsed["title"] == "Great Experience"
        assert parsed["name"] == "Ahmed Rifai"
        assert parsed["date"] == "2026-10-08"
        assert "productivity gains" in parsed["feedback"]
        assert "enterprise workflows" in parsed["feedback"]

        # Test directory parsing (should skip bad.txt gracefully)
        batch_items = parse_feedback_directory(tmp_dir)
        assert len(batch_items) == 1
        assert batch_items[0]["name"] == "Ahmed Rifai"

        # Test API POST with mock response
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.text = '{"status": "created", "id": 1}'

        with patch("requests.post", return_value=mock_resp) as mock_post:
            ok, status, resp_txt = post_feedback_to_api("http://example.com/feedback", parsed)
            assert ok is True
            assert status == 201
            assert "created" in resp_txt
            assert mock_post.called

        # Test batch upload with mock session
        mock_session_post = MagicMock(return_value=mock_resp)
        with patch.object(requests.Session, "post", mock_session_post):
            batch_result = batch_post_feedbacks("http://example.com/feedback", batch_items)
            assert batch_result["total"] == 1
            assert batch_result["success_count"] == 1
            assert batch_result["failure_count"] == 0

        print("[PASS] Module 2 (Web Services & REST APIs): All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module2()
