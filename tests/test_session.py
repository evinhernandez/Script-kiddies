import unittest
from unittest.mock import patch
from src.core.session import SessionManager
from src.core.engine import AttackResult
from src.utils.scoring import ScoreResult, ScoringStatus

class TestSessionManager(unittest.TestCase):
    def setUp(self):
        # Force an in-memory SQLite DB so tests don't pollute the real vault
        with patch('src.core.config.config.db.db_path', ':memory:'):
            self.sm = SessionManager()

    def test_save_and_retrieve_session(self):
        score = ScoreResult(
            result=ScoringStatus.SUCCESS, 
            confidence=1.0, 
            score=1.0, 
            signals=["test_signal"], 
            details="Test details"
        )
        ar = AttackResult(
            module="test.module", 
            provider="openai", 
            model="gpt-4o", 
            payload="inject", 
            response="pwned", 
            score=score,
            metadata={"turns": 1}
        )
        
        # Save to DB
        session_id = self.sm.save(ar)
        self.assertIsNotNone(session_id)
        
        # Retrieve and verify
        record = self.sm.get(session_id)
        self.assertIsNotNone(record)
        self.assertEqual(record.module_name, "test.module")
        self.assertEqual(record.result, "success")
        self.assertEqual(record.payload, "inject")
        self.assertIn("test_signal", record.signals)

    def test_stats_aggregation(self):
        # Create one success and one failure
        score_succ = ScoreResult(result=ScoringStatus.SUCCESS, confidence=1.0, score=1.0, signals=[], details="")
        score_fail = ScoreResult(result=ScoringStatus.FAILURE, confidence=1.0, score=0.0, signals=[], details="")
        
        ar_succ = AttackResult(module="test", provider="test", model="test", payload="test", response="test", score=score_succ)
        ar_fail = AttackResult(module="test", provider="test", model="test", payload="test", response="test", score=score_fail)
        
        self.sm.save(ar_succ)
        self.sm.save(ar_fail)
        
        # Verify stats math
        stats = self.sm.stats()
        self.assertEqual(stats["total_attacks"], 2)
        self.assertEqual(stats["successes"], 1)
        self.assertEqual(stats["failures"], 1)
        self.assertEqual(stats["success_rate"], 0.5)

if __name__ == '__main__':
    unittest.main()
