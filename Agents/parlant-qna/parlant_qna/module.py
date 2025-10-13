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

from contextlib import AsyncExitStack
import os

from lagom import Container
from parlant.core.nlp.service import NLPService
from parlant.core.services.tools.plugins import PluginServer
from parlant.core.services.tools.service_registry import ServiceRegistry

from parlant_qna.app import create_persistent_app
from parlant_qna.server import create_server

PORT = int(os.environ.get("PARLANT_QNA_PORT", 8807))
SERVER_INSTANCE: PluginServer | None = None
EXIT_STACK: AsyncExitStack | None = None


async def initialize_module(container: Container) -> None:
    global SERVER_INSTANCE, EXIT_STACK

    EXIT_STACK = AsyncExitStack()

    qna_app = await EXIT_STACK.enter_async_context(
        create_persistent_app(container[NLPService])
    )

    SERVER_INSTANCE = create_server(
        port=PORT,
        qna_app=qna_app,
        hosted=True,
    )

    await EXIT_STACK.enter_async_context(SERVER_INSTANCE)

    await container[ServiceRegistry].update_tool_service(
        name="qna",
        kind="sdk",
        url=f"http://127.0.0.1:{PORT}",
        transient=True,
    )


async def shutdown_module() -> None:
    if SERVER_INSTANCE:
        await SERVER_INSTANCE.shutdown()

    if EXIT_STACK:
        await EXIT_STACK.aclose()
