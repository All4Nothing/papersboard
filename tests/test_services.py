import unittest
from app.services.arxiv_service import fetch_latest_papers

class TestArxivService(unittest.TestCase):
    def test_fetch_latest_papers(self):
        papers = fetch_latest_papers()
        self.assertIsInstance(papers, dict)
        self.assertIn("status", papers)