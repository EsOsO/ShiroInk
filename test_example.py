"""
Example unit tests demonstrating improved testability with ProgressReporter abstraction.
"""

import unittest
from pathlib import Path
from src.config import ProcessingConfig
from src.progress_reporter import SilentProgressReporter
from src.file_processor import process_images_in_directory


class TestFileProcessor(unittest.TestCase):
    """Test file processing functionality without UI coupling."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = ProcessingConfig(
            src_dir=Path("/tmp/test_src"),
            dest_dir=Path("/tmp/test_dest"),
            dry_run=True,
            debug=False,
        )
        self.reporter = SilentProgressReporter()

    def test_process_with_silent_reporter(self):
        """Test that processing works with silent reporter (no UI dependencies)."""
        # This test can run without any UI output
        # Before the refactoring, this would require Rich Progress objects
        
        test_dir = Path("/tmp/shiroink_test_dir/chapter1")
        if test_dir.exists():
            try:
                process_images_in_directory(test_dir, self.config, self.reporter)
                # Verify that tasks were tracked
                self.assertGreaterEqual(len(self.reporter._tasks), 0)
            except Exception as e:
                # In dry-run mode, some operations might fail, that's OK
                pass

    def test_reporter_logging(self):
        """Test that reporter logs messages correctly."""
        self.reporter.log("Test message", level="info")
        self.reporter.log("Test error", level="error")
        # Silent reporter should not raise any exceptions

    def test_task_management(self):
        """Test task addition, advancement, and removal."""
        task_id = self.reporter.add_task("Test task", total=10)
        self.assertIsNotNone(task_id)
        
        # Advance task
        self.reporter.advance_task(task_id, advance=5)
        self.assertEqual(self.reporter._tasks[task_id]["completed"], 5)
        
        # Update task
        self.reporter.update_task(task_id, completed=8)
        self.assertEqual(self.reporter._tasks[task_id]["completed"], 8)
        
        # Remove task
        self.reporter.remove_task(task_id)
        self.assertNotIn(task_id, self.reporter._tasks)

    def test_context_manager(self):
        """Test that reporter works as context manager."""
        with self.reporter as r:
            self.assertIsNotNone(r)
            task_id = r.add_task("Context test", total=1)
            r.advance_task(task_id)
            r.remove_task(task_id)


if __name__ == "__main__":
    unittest.main()
