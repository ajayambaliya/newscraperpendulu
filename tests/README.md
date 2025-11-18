# Test Suite

This directory contains the test suite for the Pendulumedu Quiz Scraper.

## Test Structure

- `test_state_manager.py` - Unit tests for the StateManager module
- `test_parser.py` - Unit tests for the QuizParser module
- `test_integration.py` - Integration tests for the complete pipeline

## Running Tests

### Run all tests
```bash
python -m pytest tests/ -v
```

### Run specific test file
```bash
python -m pytest tests/test_state_manager.py -v
python -m pytest tests/test_parser.py -v
python -m pytest tests/test_integration.py -v
```

### Run with coverage report
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## Test Coverage

### State Manager Tests (9 tests)
- Loading empty and existing tracking files
- URL checking and marking as processed
- File persistence across instances
- Duplicate URL handling

### Parser Tests (9 tests)
- Question extraction from HTML
- Option parsing with various formats
- Correct answer identification
- Explanation extraction
- Error handling for malformed HTML

### Integration Tests (7 tests)
- Complete pipeline processing
- Already-processed URL handling
- Error recovery scenarios (scraper, parser, telegram failures)
- Multiple quiz processing
- Partial failure handling

## Total: 25 tests

All tests use Python's built-in `unittest` framework and can be run with pytest.
