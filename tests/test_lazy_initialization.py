from unittest.mock import Mock

from starmerge import create_tailwind_merge
from starmerge.lib.default_config import get_default_config


def test_lazy_initialization():
    init_mock = Mock(side_effect=get_default_config)
    tailwind_merge = create_tailwind_merge(init_mock)

    assert init_mock.call_count == 0

    tailwind_merge()
    assert init_mock.call_count == 1

    tailwind_merge()
    tailwind_merge("")
    tailwind_merge("px-2 p-3 p-4")
    assert init_mock.call_count == 1
