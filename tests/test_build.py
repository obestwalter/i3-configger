import os
from pathlib import Path

import pytest

from i3configger import build, paths, config, partials

HERE = Path(__file__).parent
EXAMPLES = HERE.parent / 'examples'
REFERENCE = HERE / 'examples'
FAKE_HEADER = """\
###############################################################################
# Built by i3configger /from/some/directory/who/cares  (some time after 1972) #
###############################################################################
"""
TEST_FOLDER_NAMES = sorted(list(
    [d.name for d in EXAMPLES.iterdir()
     if d.is_dir() and not str(d.name).startswith('_')]))


@pytest.mark.parametrize("container", TEST_FOLDER_NAMES)
def test_build(container, monkeypatch):
    monkeypatch.setattr(
        paths, 'get_i3_config_path', lambda: EXAMPLES / container)
    monkeypatch.setattr(build, 'make_header', lambda _: FAKE_HEADER)
    configPath = paths.get_my_config_path()
    assert configPath.exists() and configPath.is_file()
    p = paths.Paths(configPath)
    if p.state.exists():
        os.unlink(p.state)
    config.State.fetch_state(p.state, partials.create(p.root))
    build.build_all(configPath)
    buildPath = configPath.parents[1]
    referencePath = REFERENCE / container
    names = [p.name for p in referencePath.iterdir()]
    assert names
    for name in names:
        resultFilePath = buildPath / name
        referenceFilePath = (referencePath / name)
        assert resultFilePath != referenceFilePath
        result = resultFilePath.read_text()
        reference = referenceFilePath.read_text()
        assert result == reference
