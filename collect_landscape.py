#!/usr/bin/env python3
"""Collect a reproducible PairTalk literature, code, and dataset landscape."""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


PAPER_QUERIES = [
    "talking head gaussian splatting",
    "audio driven 3D gaussian avatar",
    "few shot personalized talking head",
    "few shot personalized 3D gaussian talking head",
    "one shot talking avatar personalization",
    "test time adaptation talking head",
    "support conditioned facial animation",
    "multilingual cross lingual talking head",
    "speaking style facial animation",
    "teacher distillation talking head animation",
    "teacher student personalized talking head",
    "same utterance paired supervision talking head",
    "paired audio motion correspondence facial animation",
    "audio motion residual retargeting facial animation",
    "few shot motion retargeting talking avatar",
    "personalized facial motion calibration speech",
    "counterfactual validation talking head adaptation",
    "uncertainty abstention speech driven facial animation",
    "conformal prediction talking head animation",
    "target specific speech driven facial animation",
    "audio conditioned facial motion velocity",
    "residual motion field talking head",
    "facial motion trajectory flow matching",
    "inverse rendering facial motion optimization",
    "differentiable renderer feedback talking head",
    "photometric supervision 3D facial motion",
    "appearance motion disentanglement 3D gaussian avatar",
    "nuisance invariant facial animation",
    "temporal high pass facial motion audio",
    "articulatory event talking head lip closure",
    "phoneme viseme constraints 3D gaussian splatting",
    "2D lifted 3D talking head motion",
    "support image supervision personalized avatar",
    "speaker specific coarticulation facial animation",
    "causal audio facial motion personalization",
    "motion appearance factorization talking avatar",
    "personalized dynamic texture talking head",
    "residual optical flow talking head",
    "speech driven 3D facial animation diffusion",
    "audio visual lip synchronization avatar",
    "speech driven 3D face dataset",
]

CODE_QUERIES = [
    "talking head gaussian splatting",
    "audio driven gaussian avatar",
    "few shot talking head 3DGS",
    "cross lingual talking head",
    "speech driven 3D facial animation",
    "personalized talking avatar",
    "talking head motion diffusion",
    "facial motion retargeting audio",
    "test time talking head adaptation",
    "personalized facial motion calibration",
    "inverse rendering facial animation",
    "appearance motion disentanglement avatar",
    "phoneme viseme talking head",
    "2D lifted 3D talking head",
    "dynamic texture talking head",
]

DATASET_QUERIES = [
    "talking head",
    "lip sync video",
    "multilingual audio visual speech",
    "facial animation speech",
    "3d facial motion speech",
    "talking face 3dmm",
    "facial motion capture audio",
    "speech driven avatar",
    "audio facial motion paired",
    "multilingual 3d facial animation",
    "talking head personalization dataset",
    "conversational 3d talking head dataset",
    "multispeaker 3d facial motion audio dataset",
    "phoneme viseme audiovisual dataset",
    "coarticulation audiovisual dataset",
    "3d face mesh speech dataset",
    "multiview talking head dataset",
]

RELEVANCE_WEIGHTS = {
    "talking head": 8,
    "gaussian splatting": 7,
    "3d gaussian": 6,
    "audio-driven": 4,
    "audio driven": 4,
    "speech-driven": 4,
    "speech driven": 4,
    "few-shot": 4,
    "few shot": 4,
    "one-shot": 4,
    "one shot": 4,
    "test-time adaptation": 5,
    "test time adaptation": 5,
    "support-conditioned": 5,
    "support conditioned": 5,
    "personalized": 4,
    "personalised": 4,
    "cross-lingual": 5,
    "cross lingual": 5,
    "multilingual": 4,
    "style": 2,
    "distillation": 3,
    "facial animation": 5,
    "facial motion": 4,
    "lip sync": 4,
    "lip-sync": 4,
    "trajectory": 3,
    "velocity field": 3,
    "motion capture": 3,
    "motion prior": 3,
    "inverse rendering": 5,
    "differentiable renderer": 5,
    "photometric supervision": 4,
    "image-level supervision": 4,
    "image level supervision": 4,
    "appearance-motion": 5,
    "appearance motion": 5,
    "nuisance": 5,
    "factorization": 3,
    "disentanglement": 3,
    "articulatory": 5,
    "coarticulation": 5,
    "viseme": 4,
    "phoneme": 3,
    "2d-lifted": 5,
    "2d lifted": 5,
    "dynamic texture": 4,
    "optical flow": 3,
    "retargeting": 4,
    "calibration": 4,
    "correspondence": 5,
    "counterfactual": 5,
    "conformal": 4,
    "uncertainty": 3,
    "abstention": 4,
    "motion": 2,
    "avatar": 2,
}

HEADERS = {
    "User-Agent": "PairTalk-research/1.0 (academic landscape collector)",
    "Accept": "application/json,text/html",
}


def get_json(url: str, params=None, timeout=45):
    response = requests.get(url, params=params, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.json()


def relevance(text: str) -> int:
    normalized = re.sub(r"\s+", " ", text.lower())
    return sum(weight for phrase, weight in RELEVANCE_WEIGHTS.items()
               if phrase in normalized)


def inverted_abstract(index):
    if not index:
        return ""
    positions = []
    for word, offsets in index.items():
        positions.extend((offset, word) for offset in offsets)
    return " ".join(word for _, word in sorted(positions))


def collect_openalex(errors):
    works = {}
    for query in PAPER_QUERIES:
        params = {
            "search": query,
            "filter": "from_publication_date:2023-01-01",
            "per-page": 100,
            "select": ("id,doi,title,publication_year,publication_date,"
                       "primary_location,best_oa_location,authorships,"
                       "cited_by_count,open_access,abstract_inverted_index,type"),
        }
        try:
            payload = get_json("https://api.openalex.org/works", params=params)
        except Exception as exc:
            errors.append({"source": "openalex", "query": query, "error": str(exc)})
            continue
        for item in payload.get("results", []):
            title = (item.get("title") or "").strip()
            abstract = inverted_abstract(item.get("abstract_inverted_index"))
            score = relevance(f"{title} {abstract}")
            if score < 4:
                continue
            doi = (item.get("doi") or "").strip().lower()
            normalized_title = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()
            key = doi or f"{normalized_title}|{item.get('publication_year')}"
            if key in works:
                existing = works[key]
                existing["matched_queries"] = sorted(set(
                    existing.get("matched_queries", []) + [query]
                ))
                existing["relevance_score"] = max(
                    existing.get("relevance_score", 0), score,
                )
                if item.get("cited_by_count", 0) > existing.get("cited_by_count", 0):
                    preserved_queries = existing["matched_queries"]
                    preserved_score = existing["relevance_score"]
                    works[key] = item
                    works[key]["matched_queries"] = preserved_queries
                    works[key]["relevance_score"] = preserved_score
            else:
                item["matched_queries"] = [query]
                item["relevance_score"] = score
                works[key] = item
        time.sleep(0.15)
    return list(works.values())


def parse_arxiv_result(result, query):
    title_el = result.select_one("p.title")
    abstract_el = result.select_one("span.abstract-full")
    authors = [a.get_text(" ", strip=True) for a in result.select("p.authors a")]
    links = {a.get_text(" ", strip=True): a.get("href")
             for a in result.select("p.list-title a[href]")}
    submitted = result.select_one("p.is-size-7")
    title = title_el.get_text(" ", strip=True) if title_el else ""
    abstract = abstract_el.get_text(" ", strip=True).replace("△ Less", "") if abstract_el else ""
    arxiv_url = links.get("arXiv:") or next(
        (href for label, href in links.items() if "arxiv" in label.lower()), None)
    arxiv_id = arxiv_url.rstrip("/").split("/")[-1] if arxiv_url else None
    return {
        "id": arxiv_id,
        "title": title,
        "abstract": abstract,
        "authors": authors,
        "submitted_text": submitted.get_text(" ", strip=True) if submitted else "",
        "url": arxiv_url,
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}" if arxiv_id else None,
        "matched_queries": [query],
        "relevance_score": relevance(f"{title} {abstract}"),
    }


def collect_arxiv(errors):
    papers = {}
    for query in PAPER_QUERIES:
        url = ("https://arxiv.org/search/?query=" + quote_plus(query) +
               "&searchtype=all&abstracts=show&order=-announced_date_first&size=100")
        try:
            response = requests.get(url, headers=HEADERS, timeout=45)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as exc:
            errors.append({"source": "arxiv", "query": query, "error": str(exc)})
            continue
        for result in soup.select("li.arxiv-result"):
            item = parse_arxiv_result(result, query)
            if not item["id"] or item["relevance_score"] < 4:
                continue
            if item["id"] in papers:
                papers[item["id"]]["matched_queries"] = sorted(set(
                    papers[item["id"]]["matched_queries"] + [query]))
            else:
                papers[item["id"]] = item
        time.sleep(0.6)
    return list(papers.values())


def collect_github(errors):
    repos = {}
    for query in CODE_QUERIES:
        try:
            payload = get_json(
                "https://api.github.com/search/repositories",
                params={"q": query, "sort": "stars", "order": "desc", "per_page": 50},
            )
        except Exception as exc:
            errors.append({"source": "github", "query": query, "error": str(exc)})
            continue
        for item in payload.get("items", []):
            text = f"{item.get('name', '')} {item.get('description') or ''}"
            score = relevance(text)
            if score < 4:
                continue
            record = {
                "full_name": item["full_name"],
                "url": item["html_url"],
                "clone_url": item["clone_url"],
                "description": item.get("description"),
                "stars": item.get("stargazers_count", 0),
                "forks": item.get("forks_count", 0),
                "updated_at": item.get("updated_at"),
                "pushed_at": item.get("pushed_at"),
                "license": (item.get("license") or {}).get("spdx_id"),
                "archived": item.get("archived", False),
                "matched_queries": [query],
                "relevance_score": score,
            }
            if record["full_name"] in repos:
                repos[record["full_name"]]["matched_queries"] = sorted(set(
                    repos[record["full_name"]]["matched_queries"] + [query]))
            else:
                repos[record["full_name"]] = record
        time.sleep(1.0)
    return list(repos.values())


def collect_huggingface(errors):
    datasets = {}
    for query in DATASET_QUERIES:
        try:
            payload = get_json(
                "https://huggingface.co/api/datasets",
                params={"search": query, "limit": 100, "full": "true"},
            )
        except Exception as exc:
            errors.append({"source": "huggingface", "query": query, "error": str(exc)})
            continue
        for item in payload:
            text = f"{item.get('id', '')} {item.get('description') or ''} {' '.join(item.get('tags', []))}"
            score = relevance(text)
            if score < 3:
                continue
            tags = item.get("tags", [])
            license_tag = next((tag.split(":", 1)[1] for tag in tags
                                if tag.startswith("license:")), None)
            size_tag = next((tag.split(":", 1)[1] for tag in tags
                             if tag.startswith("size_categories:")), None)
            record = {
                "id": item["id"],
                "url": f"https://huggingface.co/datasets/{item['id']}",
                "description": item.get("description"),
                "downloads": item.get("downloads", 0),
                "likes": item.get("likes", 0),
                "created_at": item.get("createdAt"),
                "last_modified": item.get("lastModified"),
                "gated": item.get("gated", False),
                "private": item.get("private", False),
                "license": license_tag,
                "size_category": size_tag,
                "tags": tags,
                "matched_queries": [query],
                "relevance_score": score,
            }
            if record["id"] in datasets:
                datasets[record["id"]]["matched_queries"] = sorted(set(
                    datasets[record["id"]]["matched_queries"] + [query]))
            else:
                datasets[record["id"]] = record
        time.sleep(0.2)
    return list(datasets.values())


def save_csv(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            cooked = dict(row)
            for key, value in cooked.items():
                if isinstance(value, (list, dict)):
                    cooked[key] = json.dumps(value, ensure_ascii=False)
            writer.writerow(cooked)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("research/catalog"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    errors = []
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "paper_queries": PAPER_QUERIES,
        "code_queries": CODE_QUERIES,
        "dataset_queries": DATASET_QUERIES,
        "openalex": collect_openalex(errors),
        "arxiv": collect_arxiv(errors),
        "github": collect_github(errors),
        "huggingface": collect_huggingface(errors),
        "errors": errors,
    }
    for source in ("openalex", "arxiv", "github", "huggingface"):
        payload[source].sort(
            key=lambda item: (item.get("relevance_score", 0),
                              item.get("cited_by_count", item.get("stars", 0))),
            reverse=True,
        )

    (args.out / "landscape.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    save_csv(args.out / "papers_openalex.csv", payload["openalex"], [
        "relevance_score", "title", "publication_date", "publication_year",
        "doi", "id", "cited_by_count", "type", "matched_queries",
        "primary_location", "best_oa_location", "open_access",
    ])
    save_csv(args.out / "papers_arxiv.csv", payload["arxiv"], [
        "relevance_score", "title", "id", "submitted_text", "authors", "url",
        "pdf_url", "matched_queries", "abstract",
    ])
    save_csv(args.out / "code_github.csv", payload["github"], [
        "relevance_score", "full_name", "url", "stars", "forks", "license",
        "updated_at", "pushed_at", "archived", "description", "matched_queries",
    ])
    save_csv(args.out / "datasets_huggingface.csv", payload["huggingface"], [
        "relevance_score", "id", "url", "downloads", "likes", "license",
        "size_category", "gated", "created_at", "last_modified", "description",
        "matched_queries", "tags",
    ])
    print(json.dumps({source: len(payload[source]) for source in
                      ("openalex", "arxiv", "github", "huggingface")}))
    if errors:
        print(f"completed with {len(errors)} source/query errors; see landscape.json")


if __name__ == "__main__":
    main()
