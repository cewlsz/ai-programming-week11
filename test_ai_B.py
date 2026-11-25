import pytest
from load_scores import load_scores


def make_file(tmp_path, text):
    path = tmp_path / "input.csv"
    path.write_text(text, encoding="utf-8-sig")
    return path


def test_valid_records(tmp_path):
    path = make_file(
        tmp_path,
        'name,score\n민수,85\n\n"김,하나",90\n',
    )
    kept, skipped = load_scores(path)
    assert kept == [("민수", 85), ("김,하나", 90)]
    assert skipped == []


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_header_only(tmp_path):
    path = make_file(tmp_path, "name,score\n")
    assert load_scores(path) == ([], [])


@pytest.mark.parametrize(
    "row",
    ["민수,80,추가", "민수,", "민수,abc", ",80"],
)
def test_invalid_record_is_skipped(tmp_path, row):
    path = make_file(
        tmp_path,
        f"name,score\n{row}\n서연,90\n",
    )
    kept, skipped = load_scores(path)

    assert kept == [("서연", 90)]
    assert len(skipped) == 1
    line_no, original, reason = skipped[0]
    assert line_no == 2
    assert original == row
    assert isinstance(reason, str)
    assert reason.strip() != ""


@pytest.mark.parametrize(
    "score, accepted",
    [(0, True), (100, True), (101, False)],
)
def test_score_boundaries(tmp_path, score, accepted):
    path = make_file(
        tmp_path, f"name,score\n민수,{score}\n"
    )
    kept, skipped = load_scores(path)

    if accepted:
        assert kept == [("민수", score)]
        assert skipped == []
    else:
        assert kept == []
        assert len(skipped) == 1
        assert skipped[0][0] == 2


def test_same_name_records_are_preserved(tmp_path):
    path = make_file(
        tmp_path, "name,score\n민수,70\n민수,95\n"
    )
    kept, skipped = load_scores(path)
    assert kept == [("민수", 70), ("민수", 95)]
    assert skipped == []