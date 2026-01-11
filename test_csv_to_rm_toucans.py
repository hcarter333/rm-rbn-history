import csv
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from csv_to_rm_toucans import cutoff_from_db

SCHEMA = """
CREATE TABLE rm_rnb_history_pres (
  id           REAL,
  tx_lng       REAL,
  tx_lat       REAL,
  rx_lng       REAL,
  rx_lat       REAL,
  timestamp    TEXT,
  dB           INTEGER,
  frequency    REAL,
  Spotter      TEXT,
  Country      TEXT,
  State        TEXT,
  County       TEXT,
  City         TEXT,
  QSL_Sent     INTEGER,
  QSL_Rx       TEXT,
  QSL_link     TEXT,
  QSL_rx_link  TEXT,
  tx_rst       INTEGER,
  park         TEXT,
  p2p_s2       TEXT,
  call         TEXT,
  skcc         TEXT,
  naqcc        INTEGER,
  f2m          REAL,
  launchangle  REAL
);
"""


def write_csv(path: Path, rows: list[list[object]]) -> None:
    headers = [
        "id",
        "tx_lng",
        "tx_lat",
        "rx_lng",
        "rx_lat",
        "timestamp",
        "dB",
        "frequency",
        "Spotter",
        "Country",
        "State",
        "County",
        "City",
        "QSL_Sent",
        "QSL_Rx",
        "QSL_link",
        "QSL_rx_link",
        "tx_rst",
        "park",
        "p2p_s2",
        "call",
        "skcc",
        "naqcc",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


def seed_db(db_path: Path, rows: list[tuple]) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA)
        if rows:
            conn.executemany(
                """
                INSERT INTO rm_rnb_history_pres (
                    id, tx_lng, tx_lat, rx_lng, rx_lat, timestamp, dB, frequency,
                    Spotter, Country, State, County, City, QSL_Sent, QSL_Rx,
                    QSL_link, QSL_rx_link, tx_rst, park, p2p_s2, call, skcc, naqcc,
                    f2m, launchangle
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )


def run_script(csv_path: Path, db_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "csv_to_rm_toucans.py", str(csv_path), "--db", str(db_path)],
        check=True,
        text=True,
        capture_output=True,
    )


def fetch_count_and_latest(db_path: Path) -> tuple[int, str]:
    with sqlite3.connect(db_path) as conn:
        count = conn.execute("select count(*) from rm_rnb_history_pres").fetchone()[0]
        latest = conn.execute("select max(timestamp) from rm_rnb_history_pres").fetchone()[0]
    return count, latest


def test_imports_only_new_rows_without_after(tmp_path: Path) -> None:
    db_path = tmp_path / "rm_toucans.db"
    csv_path = tmp_path / "rm_rnb_history_pres.csv"

    seed_db(
        db_path,
        [
            (
                1.0,
                -100.0,
                40.0,
                -101.0,
                41.0,
                "2024-01-01T00:00:00",
                10,
                7.0,
                "SPOT1",
                "USA",
                "CO",
                "Test",
                "City",
                1,
                "N",
                "",
                "",
                599,
                "",
                "",
                "CALL1",
                "",
                1234,
                None,
                None,
            )
        ],
    )

    write_csv(
        csv_path,
        [
            [
                1.0,
                -100.0,
                40.0,
                -101.0,
                41.0,
                "2024/01/01 00:00:00",
                10,
                7.0,
                "SPOT1",
                "USA",
                "CO",
                "Test",
                "City",
                1,
                "N",
                "",
                "",
                599,
                "",
                "",
                "CALL1",
                "",
                1234,
            ],
            [
                2.0,
                -100.0,
                40.0,
                -101.0,
                41.0,
                "2024/01/02 00:00:00",
                11,
                7.1,
                "SPOT2",
                "USA",
                "CO",
                "Test",
                "City",
                1,
                "N",
                "",
                "",
                599,
                "",
                "",
                "CALL2",
                "",
                1234,
            ],
            [
                3.0,
                -100.0,
                40.0,
                -101.0,
                41.0,
                "2024/01/03 00:00:00",
                12,
                7.2,
                "SPOT3",
                "USA",
                "CO",
                "Test",
                "City",
                1,
                "N",
                "",
                "",
                599,
                "",
                "",
                "CALL3",
                "",
                1234,
            ],
            [
                4.0,
                -100.0,
                40.0,
                -101.0,
                41.0,
                "2024/01/04 00:00:00",
                13,
                7.3,
                "SPOT4",
                "USA",
                "CO",
                "Test",
                "City",
                1,
                "N",
                "",
                "",
                599,
                "",
                "",
                "CALL4",
                "",
                1234,
            ],
            [
                5.0,
                -100.0,
                40.0,
                -101.0,
                41.0,
                "2024/01/05 00:00:00",
                14,
                7.4,
                "SPOT5",
                "USA",
                "CO",
                "Test",
                "City",
                1,
                "N",
                "",
                "",
                599,
                "",
                "",
                "CALL5",
                "",
                1234,
            ],
        ],
    )

    result = run_script(csv_path, db_path)
    assert "Inserted 4 rows" in result.stdout
    count, latest = fetch_count_and_latest(db_path)
    assert count == 5
    assert latest == "2024-01-05T00:00:00"


def test_imports_all_rows_when_db_is_empty(tmp_path: Path) -> None:
    db_path = tmp_path / "rm_toucans.db"
    csv_path = tmp_path / "rm_rnb_history_pres.csv"

    seed_db(db_path, [])
    write_csv(
        csv_path,
        [
            [
                1.0,
                -100.0,
                40.0,
                -101.0,
                41.0,
                "2024/01/02 00:00:00",
                11,
                7.1,
                "SPOT2",
                "USA",
                "CO",
                "Test",
                "City",
                1,
                "N",
                "",
                "",
                599,
                "",
                "",
                "CALL2",
                "",
                1234,
            ],
            [
                2.0,
                -100.0,
                40.0,
                -101.0,
                41.0,
                "2024/01/03 00:00:00",
                12,
                7.2,
                "SPOT3",
                "USA",
                "CO",
                "Test",
                "City",
                1,
                "N",
                "",
                "",
                599,
                "",
                "",
                "CALL3",
                "",
                1234,
            ],
            [
                3.0,
                -100.0,
                40.0,
                -101.0,
                41.0,
                "2024/01/04 00:00:00",
                13,
                7.3,
                "SPOT4",
                "USA",
                "CO",
                "Test",
                "City",
                1,
                "N",
                "",
                "",
                599,
                "",
                "",
                "CALL4",
                "",
                1234,
            ],
            [
                4.0,
                -100.0,
                40.0,
                -101.0,
                41.0,
                "2024/01/05 00:00:00",
                14,
                7.4,
                "SPOT5",
                "USA",
                "CO",
                "Test",
                "City",
                1,
                "N",
                "",
                "",
                599,
                "",
                "",
                "CALL5",
                "",
                1234,
            ],
            [
                5.0,
                -100.0,
                40.0,
                -101.0,
                41.0,
                "2024/01/06 00:00:00",
                15,
                7.5,
                "SPOT6",
                "USA",
                "CO",
                "Test",
                "City",
                1,
                "N",
                "",
                "",
                599,
                "",
                "",
                "CALL6",
                "",
                1234,
            ],
        ],
    )

    run_script(csv_path, db_path)
    count, latest = fetch_count_and_latest(db_path)
    assert count == 5
    assert latest == "2024-01-06T00:00:00"


def test_cutoff_from_db_requires_db_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        cutoff_from_db(tmp_path / "missing.db")


def test_cutoff_from_db_requires_table(tmp_path: Path) -> None:
    db_path = tmp_path / "rm_toucans.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute("create table example(id integer)")
    with pytest.raises(sqlite3.OperationalError, match="rm_rnb_history_pres"):
        cutoff_from_db(db_path)


def test_reports_earliest_and_latest_inserted_timestamps(tmp_path: Path) -> None:
    db_path = tmp_path / "rm_toucans.db"
    csv_path = tmp_path / "rm_rnb_history_pres.csv"

    existing_rows = []
    csv_rows = []
    for idx in range(1, 11):
        csv_rows.append(
            [
                float(idx),
                -100.0,
                40.0,
                -101.0,
                41.0,
                f"2024/02/{idx:02d} 12:00:00",
                10 + idx,
                7.0 + idx / 10,
                f"SPOT{idx}",
                "USA",
                "CO",
                "Test",
                "City",
                1,
                "N",
                "",
                "",
                599,
                "",
                "",
                f"CALL{idx}",
                "",
                1234,
            ]
        )
        if idx <= 5:
            existing_rows.append(
                (
                    float(idx),
                    -100.0,
                    40.0,
                    -101.0,
                    41.0,
                    f"2024-02-{idx:02d}T12:00:00",
                    10 + idx,
                    7.0 + idx / 10,
                    f"SPOT{idx}",
                    "USA",
                    "CO",
                    "Test",
                    "City",
                    1,
                    "N",
                    "",
                    "",
                    599,
                    "",
                    "",
                    f"CALL{idx}",
                    "",
                    1234,
                    None,
                    None,
                )
            )

    seed_db(db_path, existing_rows)
    write_csv(csv_path, csv_rows)

    result = run_script(csv_path, db_path)
    assert "Inserted 5 rows" in result.stdout
    assert "Earliest inserted timestamp: 2024-02-06T12:00:00" in result.stdout
    assert "Latest inserted timestamp: 2024-02-10T12:00:00" in result.stdout
