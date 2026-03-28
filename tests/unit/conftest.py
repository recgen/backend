import pytest

from tests.unit.fakes.persistence import DummyCommitter


@pytest.fixture
def committer() -> DummyCommitter:
    return DummyCommitter()
