# Copyright 2024 Emcie Co Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from contextlib import contextmanager
from typing import (
    Any,
    Iterator,
)

from parlant.adapters.nlp.openai_service import GPT_4o
from parlant.core.common import DefaultBaseModel
from parlant.core.loggers import LogLevel, Logger


class NLPTestSchema(DefaultBaseModel):
    answer: bool


class _TestLogger(Logger):
    def __init__(self) -> None:
        self.logger = logging.getLogger("TestLogger")

    def set_level(self, log_level: LogLevel) -> None:
        self.logger.setLevel(
            {
                LogLevel.DEBUG: logging.DEBUG,
                LogLevel.INFO: logging.INFO,
                LogLevel.WARNING: logging.WARNING,
                LogLevel.ERROR: logging.ERROR,
                LogLevel.CRITICAL: logging.CRITICAL,
            }[log_level]
        )

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)

    @contextmanager
    def operation(self, name: str, props: dict[str, Any] = {}) -> Iterator[None]:
        yield

    @contextmanager
    def scope(self, scope_id: str) -> Iterator[None]:
        yield


async def nlp_test(context: str, condition: str) -> bool:
    schematic_generator = GPT_4o[NLPTestSchema](logger=_TestLogger())

    inference = await schematic_generator.generate(
        prompt=f"""\
Given a context and a condition, determine whether the
condition applies with respect to the given context.
If the condition applies, the answer is true;
otherwise, the answer is false.

Context: ###
{context}
###

Condition: ###
{condition}
###

Output JSON structure: ###
{{
    answer: <BOOL>
}}
###

Example #1: ###
{{
    answer: true
}}
###

Example #2: ###
{{
    answer: false
}}
###
""",
        hints={"temperature": 0.0, "strict": True},
    )
    return inference.content.answer
