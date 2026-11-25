import pytest
from load_scores import load_scores


def make_csv(tmp_path, content):
    path = tmp_path / "scores.csv"
    path.write_text(content, encoding="utf-8-sig")
    return path


def test_normal_scores(tmp_path):
    path = make_csv(tmp_path, "name,score\n민수,85\n서연,92\n")
    kept, skipped = load_scores(path)
    assert kept == [("민수", 85), ("서연", 92)]
    assert skipped == []


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_header_only(tmp_path):
    path = make_csv(tmp_path, "name,score\n")
    assert load_scores(path) == ([], [])


@pytest.mark.parametrize(
    "score, valid",
    [(-1, False), (0, True), (1, True),
     (99, True), (100, True), (101, False)],
)
def test_score_boundaries(tmp_path, score, valid):
    path = make_csv(tmp_path, f"name,score\n민수,{score}\n")
    kept, skipped = load_scores(path)

    if valid:
        assert kept == [("민수", score)]
        assert skipped == []
    else:
        assert kept == []
        assert skipped == [
            (2, f"민수,{score}", "점수가 0~100 밖")
        ]


@pytest.mark.parametrize(
    "row, reason",
    [
        ("민수", "열 개수가 2가 아님"),
        ("민수,80,추가", "열 개수가 2가 아님"),
        (",80", "이름이 비어 있음"),
        ("민수,", "점수가 비어 있음"),
        ("민수,abc", "점수가 정수가 아님"),
        ("민수,80.5", "점수가 정수가 아님"),
    ],
)
def test_invalid_rows(tmp_path, row, reason):
    path = make_csv(
        tmp_path, f"name,score\n{row}\n서연,90\n"
    )
    kept, skipped = load_scores(path)
    assert kept == [("서연", 90)]
    assert skipped == [(2, row, reason)]


def test_blank_lines_spaces_and_comma(tmp_path):
    path = make_csv(
        tmp_path,
        'name,score\n\n 민수 , 80 \n"김,하나",90\n',
    )
    kept, skipped = load_scores(path)
    assert kept == [("민수", 80), ("김,하나", 90)]
    assert skipped == []


def test_duplicate_names_are_kept(tmp_path):
    path = make_csv(tmp_path, "name,score\n민수,80\n민수,90\n")
    kept, skipped = load_scores(path)
    assert kept == [("민수", 80), ("민수", 90)]
    assert skipped == []