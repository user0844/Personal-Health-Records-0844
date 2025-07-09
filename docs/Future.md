# Future Features and Improvements

## 1. Configurable Expected Status Codes
- Allow the expected HTTP status codes for ABDM API responses to be set via a class attribute or Django settings.
- This will make the codebase more robust to changes in the ABDM API and easier to maintain.

## 2. Lean Testing for API Integrations
- Use parameterized and mocked tests to cover key scenarios (success, common error codes, network errors, unexpected responses) instead of testing every permutation of headers, bodies, and URLs.
- This will keep the test suite fast and maintainable while ensuring good coverage.

## 3. Error Message Sanitization
- Separate internal log messages from user-facing API responses.
- Only return safe, user-friendly error messages to clients, and avoid exposing sensitive internal details.
- Consider implementing this in middleware when connecting frontend and backend.

