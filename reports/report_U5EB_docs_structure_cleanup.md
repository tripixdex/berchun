# U5E.B — Repository Docs Structure Cleanup + Link Integrity Validation

## 1. Scope and objective
- Scope ID: `U5E.B`
- Scope name: `Repository docs structure cleanup + link integrity validation`
- Objective: навести порядок в repo documentation surface без изменения solver/runtime semantics:
  - разложить `docs/` по смысловым группам;
  - переписать все repo-local ссылки на новые пути;
  - убрать из корня очевидные stray artifacts, которые уже имеют естественное место в структуре;
  - подтвердить, что documented regression command из `README.md` остаётся зелёной после реорганизации.

## 2. Files inspected
- `docs/`
- `README.md`
- `src/cli.py`
- `tests/test_delivery_guide_docx_runtime.py`
- `tests/test_delivery_guide_pdf_runtime.py`
- `tests/test_pdf_surface_integrity.py`
- `tests/_delivery_support.py`
- `reports/master_report.md`
- `runs/`
- `inputs/examples/`

## 3. Commands run
- `rg --files docs`
- `find docs -maxdepth 3 | sort`
- `rg -n "docs/..." README.md docs src tests reports`
- `find . -maxdepth 1 \( -type f -o -type d \) | sort`
- `sed -n '1,80p' <root-level microops file before move>`
- `python3 -m unittest discover -s tests -v`

## 4. What disorder was found
- `docs/` содержал плоский набор из project/spec, governance, report, delivery, UX и methodical документов без явных смысловых групп.
- В корне `docs/` отдельно лежал lower-level methodical decomposition file `METHODICAL_MICROOPS_1_1_STEP4.md`, хотя он относится к той же methodical ветке.
- `reports/` тоже остаётся плоским, но там уже плотная сетка перекрёстных ссылок; broad migration в этом pass была бы рискованной и несоразмерной user request.

## 5. What was changed
- В `docs/` созданы смысловые разделы:
  - `docs/project/`
  - `docs/governance/`
  - `docs/report/`
  - `docs/delivery/`
  - `docs/ux/`
  - `docs/methodical/architecture/`
  - `docs/methodical/content/`
  - `docs/methodical/microops/`
- Все соответствующие документы перенесены в эти разделы.
- Добавлен навигационный индекс `docs/README.md`.
- Root-level methodical microops file перенесён в `docs/methodical/microops/`.
- Переписаны repo-local ссылки на новые doc paths в:
  - `README.md`
  - `docs/`
  - `src/`
  - `tests/`
  - `reports/`
- `src/cli.py` теперь смотрит на новые canonical guide source paths внутри `docs/methodical/content/`.

## 6. What was validated
- По `README.md` канонический test command — `python3 -m unittest discover -s tests -v`; именно он использован как authoritative regression check.
- Полный documented regression run завершился успешно:
  - `Ran 72 tests in 316.880s`
  - `OK`
- По repo text surface больше не осталось ссылок на старые top-level doc paths вида `docs/<old_file>.md` в `README.md`, `docs/`, `src/`, `tests/` и `reports/`.
- `docs/` теперь читается как смысловая иерархия, а не как плоская mixed-surface папка.

## 7. What intentionally remained unchanged
- solver logic
- delivery semantics
- build semantics
- report truth
- guide truth/content
- historical flat structure `reports/`
- truth-bearing generated artifacts under `inputs/`, `out/`, `figures/`, `report/`

## 8. Scope complete? YES/NO
- `YES`

## 9. Exact next recommendation
- Считать docs housekeeping завершённым.
- Не открывать broad migration для `reports/` в фоне; если она нужна, оформлять как отдельный scope с explicit link-rewrite plan и отдельной полной валидацией.
- Для будущих regression checks использовать documented command из `README.md`: `python3 -m unittest discover -s tests -v`.
