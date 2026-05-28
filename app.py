from __future__ import annotations

import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from periodic_table import CLASS_ALIASES, ELEMENTS


HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "3000"))
BASE_DIR = Path(__file__).parent
PUBLIC_DIR = BASE_DIR / "public"

app = FastAPI(
    title="API Tableau Periodique",
    description="API pour consulter les elements du tableau periodique.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")


def normalize(value: str) -> str:
    return value.strip().lower()


def find_element(identifier: str) -> dict | None:
    value = normalize(identifier)

    if value.isdigit():
        atomic_number = int(value)
        return next((element for element in ELEMENTS if element["atomicNumber"] == atomic_number), None)

    return next((element for element in ELEMENTS if normalize(element["symbol"]) == value), None)


def find_elements_by_class(class_name: str) -> list[dict]:
    value = normalize(class_name)
    canonical_class = CLASS_ALIASES.get(value, value)

    return [
        element
        for element in ELEMENTS
        if element["class"] == canonical_class or element["category"] == canonical_class
    ]


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(PUBLIC_DIR / "index.html")


@app.get("/elements", tags=["elements"])
def get_all_elements() -> dict:
    return {"count": len(ELEMENTS), "data": ELEMENTS}


@app.get("/elements/{identifier}", tags=["elements"])
def get_element(identifier: str) -> dict:
    element = find_element(identifier)

    if element is None:
        raise HTTPException(
            status_code=404,
            detail="Aucun element trouve pour ce numero atomique ou ce symbole",
        )

    return {"data": element}


@app.get("/classes/{class_name}", tags=["classes"])
def get_elements_by_class(class_name: str) -> dict:
    elements = find_elements_by_class(class_name)

    if not elements:
        raise HTTPException(status_code=404, detail="Aucun element trouve pour cette classe")

    return {"count": len(elements), "data": elements}


if __name__ == "__main__":
    uvicorn.run("app:app", host=HOST, port=PORT, reload=True)
