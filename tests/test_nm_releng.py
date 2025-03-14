# Copyright (c) 2025 - present / Neuralmagic, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from importlib.metadata import version
from pathlib import Path
from xml.dom import minidom

import pytest


def test_plugin_loaded(pytester: pytest.Pytester):
    """Verify the plugin is loaded by pytest"""

    plugin_version = version("pytest-nm-releng")

    pytester.makepyfile("""
        def test_pass():
            pass
    """)

    result = pytester.runpytest()
    result.stdout.fnmatch_lines([f"plugins:*nm-releng-{plugin_version}*"])


def test_plugin_adds_junit_args(
    pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
):
    """Verify the plugin adds the expected junit args"""

    monkeypatch.setenv("NMRE_JUNIT_BASE", "results")
    monkeypatch.setenv("NMRE_JUNIT_PREFIX", "report-")

    # parse pytest configuration and make sure it sets the flag
    cf = pytester.parseconfigure()
    actual = cf.getoption("--junit-xml")
    assert isinstance(actual, str)
    assert actual.startswith("results")

    # run pytest and make sure it generates an XML file
    pytester.makepyfile("""
        def test_pass():
            pass
    """)
    result = pytester.runpytest()
    assert "generated xml file:" in result.stdout.str()

    # make sure the generated XML file is named correctly and exists
    pattern = re.compile(r"generated xml file: (.*?(?:\.xml))")
    match = pattern.search(result.stdout.str())
    assert match is not None
    xml_file = Path(match[1])
    assert xml_file.exists()
    assert xml_file.parent.name == "results"
    assert xml_file.name.startswith("report-")
    assert re.compile(r"\d{10,}\.\d+\.xml").fullmatch(
        xml_file.name.removeprefix("report-")
    )


@pytest.mark.parametrize("properties", [["courses=3"], ["courses=3", "dessert=true"]])
def test_plugin_adds_case_properties(
    pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch, properties: list[str]
):
    monkeypatch.delenv("NMRE_JUNIT_BASE", raising=False)
    pytester.makepyfile("""
        def test_pass():
            pass
        def test_pass_2():
            pass
    """)

    xml_path = pytester.path.joinpath("junit.xml")
    result = pytester.runpytest(
        "--junitxml", xml_path, "--testcase-property", *properties
    )
    assert result.ret == 0

    dom = minidom.parse(str(xml_path))
    cases = dom.getElementsByTagName("testcase")
    assert len(cases) == 2

    for case in cases:
        case_properties = case.getElementsByTagName("property")
        assert len(case_properties) == len(properties)

        props: list[str] = []
        for case_property in case_properties:
            joined = "=".join(
                [
                    case_property.getAttribute("name"),
                    case_property.getAttribute("value"),
                ]
            )
            props.append(joined)
        assert sorted(props) == sorted(properties)


@pytest.mark.parametrize("properties", [["courses=3"], ["courses=3", "dessert=true"]])
def test_plugin_adds_suite_properties(
    pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch, properties: list[str]
):
    monkeypatch.delenv("NMRE_JUNIT_BASE", raising=False)
    pytester.makepyfile("""
        def test_pass():
            pass
    """)

    xml_path = pytester.path.joinpath("junit.xml")
    result = pytester.runpytest(
        "--junitxml", xml_path, "--testsuite-property", *properties
    )
    assert result.ret == 0

    dom = minidom.parse(str(xml_path))
    suites = dom.getElementsByTagName("testsuite")
    assert len(suites) == 1

    suite_properties = suites[0].getElementsByTagName("property")
    assert len(suite_properties) == len(properties)

    props: list[str] = []
    for suite_property in suite_properties:
        joined = "=".join(
            [
                suite_property.getAttribute("name"),
                suite_property.getAttribute("value"),
            ]
        )
        props.append(joined)
    assert sorted(props) == sorted(properties)
