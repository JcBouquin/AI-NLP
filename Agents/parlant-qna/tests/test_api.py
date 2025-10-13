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

from collections.abc import AsyncIterator
import httpx
from pytest import fixture

from parlant_qna.app import create_transient_app
from parlant_qna.server import create_server


@fixture
async def api() -> AsyncIterator[httpx.AsyncClient]:
    port = 8899

    async with create_transient_app() as app:
        async with create_server(port=port, qna_app=app) as server:
            print("server started")
            async with httpx.AsyncClient(
                base_url=f"http://localhost:{port}",
                follow_redirects=True,
                timeout=60,
            ) as client:
                yield client
            await server.shutdown()


async def test_crud(api: httpx.AsyncClient) -> None:
    response = await api.post(
        "/questions",
        json={
            "variants": ["Who is Bubble Joe"],
            "answer": "He is the king of Bubbleland",
        },
    )

    question_id = response.json()["question_id"]

    response = await api.get(f"/questions/{question_id}")

    question = response.json()

    assert len(question["variants"]) == 1
    assert question["variants"][0] == "Who is Bubble Joe"
    assert question["answer"] == "He is the king of Bubbleland"

    await api.patch(
        f"/questions/{question_id}",
        json={
            "variants": ["Who is Bubble Joseph"],
            "answer": "He is the prince of Bubbleland",
        },
    )

    response = await api.get(f"/questions/{question_id}")

    question = response.json()

    assert len(question["variants"]) == 1
    assert question["variants"][0] == "Who is Bubble Joseph"
    assert question["answer"] == "He is the prince of Bubbleland"

    response = await api.get("/questions")

    questions = response.json()

    assert len(questions) == 1
    assert question in questions

    await api.delete(f"/questions/{question_id}")

    response = await api.get("/questions")

    questions = response.json()

    assert len(questions) == 0
