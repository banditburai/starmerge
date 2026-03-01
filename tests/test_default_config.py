from starmerge import get_default_config


def test_default_config_has_correct_types():
    default_config = get_default_config()

    assert default_config["cache_size"] == 500
    assert default_config.get("nonExistent") is None
    assert default_config["class_groups"]["display"][0] == "block"

    overflow_group = default_config["class_groups"]["overflow"][0]
    assert overflow_group["overflow"][0] == "auto"
    assert overflow_group.get("nonExistent") is None
