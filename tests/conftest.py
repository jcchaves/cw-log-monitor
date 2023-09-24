import asyncio
import pytest


@pytest.fixture
def test_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.stop()
