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

from dataclasses import asdict
from functools import partial
from typing import Awaitable, Callable, cast

from fastapi import Body, FastAPI, HTTPException, Query, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from parlant.sdk import PluginServer, ToolContext, ToolResult, tool

from parlant_qna.app import App


def get_qna_app(context: ToolContext) -> App:
    return cast(App, context.plugin_data["qna_app"])


@tool
async def find_answer(context: ToolContext, query: str) -> ToolResult:
    qna_app = get_qna_app(context)

    answer = await qna_app.ask_question(query)

    return ToolResult(
        data=answer.content,
        metadata={
            "references": [asdict(r) for r in answer.references],
            "evaluation": answer.evaluation,
        },
    )


async def wrap_with_management_endpoints(qna_app: App, api: FastAPI) -> FastAPI:
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @api.middleware("http")
    async def log_request(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        with qna_app.logger.operation(
            f"HTTP Request: {request.method} {request.url.path}"
        ):
            return await call_next(request)

    @api.get("/questions")
    async def list_questions(verbose: bool = Query(default=False)) -> JSONResponse:
        questions = await qna_app.list_questions()

        if verbose:
            return JSONResponse(content=[asdict(q) for q in questions])
        else:
            return JSONResponse(
                content=[{"id": q.id, "title": q.variants[0]} for q in questions]
            )

    @api.post("/questions")
    async def create_question(
        variants: list[str] = Body(),
        answer: str = Body(),
    ) -> JSONResponse:
        question = await qna_app.create_question(variants, answer)

        return JSONResponse(
            {"question_id": question.id},
            status_code=status.HTTP_201_CREATED,
        )

    @api.patch("/questions/{question_id}")
    async def patch_question(
        question_id: str,
        variants: list[str] | None = Body(default=None),
        answer: str | None = Body(default=None),
    ) -> JSONResponse:
        try:
            question = await qna_app.update_question(question_id, variants, answer)
            return JSONResponse(content=asdict(question))
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question '{question_id}' not found",
            )

    @api.get("/questions/{question_id}")
    async def read_question(question_id: str) -> JSONResponse:
        try:
            question = await qna_app.read_question(question_id)
            return JSONResponse(content=asdict(question))
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question '{question_id}' not found",
            )

    @api.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT,)
    async def delete_question(question_id: str) -> None:
        await qna_app.delete_question(question_id)

    @api.post("/answers")
    async def answer(query: str = Body(embed=True)) -> JSONResponse:
        answer = await qna_app.ask_question(query)

        return JSONResponse(
            {
                "answer": answer.content,
                "evaluation": answer.evaluation,
                "references": [asdict(r) for r in answer.references],
            }
        )

    @api.post("/reports")
    async def create_report(sample_percentage: int = Body(embed=True)) -> JSONResponse:
        report_id = await qna_app.create_report(sample_percentage)
        return JSONResponse(content={"report_id": report_id})

    @api.get("/reports/{report_id}")
    async def read_report(report_id: str) -> JSONResponse:
        report = await qna_app.read_report(report_id)

        return JSONResponse(
            content={
                "report": {
                    "status": report.status,
                    "expected_samples": report.expected_samples,
                    "completed_samples": len(report.samples),
                    "hallucinations": {
                        s.question_id: {
                            "query": s.variant,
                            "answer": s.answer.content,
                            "references": [asdict(r) for r in s.answer.references],
                            "entities": s.answer.extracted_entities,
                            "issue": s.hallucination,
                        }
                        for s in report.samples
                        if s.hallucination
                    },
                    "matrix": {
                        "tp": report.true_positives,
                        "tn": report.true_negatives,
                        "fp": report.false_positives,
                        "fn": report.false_negatives,
                        "ptp": len(
                            [
                                s
                                for s in report.samples
                                if s.answer.grade == "partial" and s.true_positive
                            ]
                        ),
                        "ptn": len(
                            [
                                s
                                for s in report.samples
                                if s.answer.grade == "partial" and s.true_negative
                            ]
                        ),
                        "pfp": len(
                            [
                                s
                                for s in report.samples
                                if s.answer.grade == "partial" and s.false_positive
                            ]
                        ),
                        "pfn": len(
                            [
                                s
                                for s in report.samples
                                if s.answer.grade == "partial" and s.false_negative
                            ]
                        ),
                    },
                    "precision": report.precision,
                    "recall": report.recall,
                    "accuracy": report.accuracy,
                    "f1": report.f1,
                }
            }
        )

    return api


def create_server(port: int, qna_app: App, hosted: bool = False) -> PluginServer:
    return PluginServer(
        tools=[find_answer],
        port=port,
        on_app_created=partial(wrap_with_management_endpoints, qna_app),
        plugin_data={"qna_app": qna_app},
        hosted=hosted,
    )
