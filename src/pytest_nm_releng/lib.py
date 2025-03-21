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


import os
import warnings
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

from uuid_utils import uuid4, uuid7


class SuffixType(Enum):
    TIMESTAMP = "timestamp"
    UUID4 = "uuid4"
    UUID7 = "uuid7"


DEFAULT_SUFFIX_TYPE = SuffixType.TIMESTAMP


def get_utc_timestamp() -> str:
    return str(datetime.now(timezone.utc).timestamp())


def generate_suffix(suffix_type: SuffixType) -> str:
    suffix_map = {
        SuffixType.TIMESTAMP: get_utc_timestamp,
        SuffixType.UUID4: lambda: str(uuid4()),
        SuffixType.UUID7: lambda: str(uuid7()),
    }
    return suffix_map.get(suffix_type, get_utc_timestamp)()


def generate_junit_flags() -> list[str]:
    if not (junitxml_base_dir := os.getenv("NMRE_JUNIT_BASE")):
        return []

    valid_suffix_types = [st.value for st in SuffixType]
    junit_suffix_type = os.getenv("NMRE_JUNIT_SUFFIX_TYPE", DEFAULT_SUFFIX_TYPE.value)
    if junit_suffix_type in valid_suffix_types:
        junit_suffix_type = SuffixType(junit_suffix_type)
    else:
        msg = (
            "NMRE_JUNIT_SUFFIX_TYPE must be one of "
            f"{', '.join(valid_suffix_types)}, got '{junit_suffix_type}'."
            f" Defaulting to '{DEFAULT_SUFFIX_TYPE.value}'."
        )
        warnings.warn(msg, UserWarning)
        junit_suffix_type = DEFAULT_SUFFIX_TYPE

    prefix = os.getenv("NMRE_JUNIT_PREFIX", "")
    junitxml_file = (
        Path(junitxml_base_dir) / f"{prefix}{generate_suffix(junit_suffix_type)}.xml"
    )

    return [f"--junit-xml={junitxml_file}"]
