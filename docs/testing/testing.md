# Testing

## API Test Automation

The TaskFlow API is covered by automated tests using:

- Pytest
- Django REST Framework APIClient
- pytest-django

## Test Coverage

The automated test suite covers:

- Authentication and authorization
- User APIs
- Workspace APIs
- Membership APIs
- Invitation APIs
- Project APIs
- Workflow APIs
- Workflow Status APIs
- Status APIs
- Sprint APIs
- Positive and negative test cases
- Role-based access control
- API validation
- Database state verification

## Testing Techniques

The test suite uses:

- Fixtures
- `conftest.py`
- Parametrization
- Assertions
- Authentication fixtures
- Database assertions
- Test classes
- HTTP status code validation

## Running Tests

```bash
pytest


### Test Results

✅ 221 tests passed