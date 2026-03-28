import pytest

from tests.unit.fakes.persistence import DummyCommitter
from tests.unit.stubs.idp import StubIdp


@pytest.fixture
def committer() -> DummyCommitter:
    return DummyCommitter()


@pytest.fixture
def idp() -> StubIdp:
    return StubIdp()
