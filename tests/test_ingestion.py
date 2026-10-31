from ingestion import read_csv_with_rejects


def test_malformed_csv_records(tmp_path):

    csv_file = tmp_path / "test_customers.csv"

    csv_file.write_text(
        "customer_id,customer_name,email,city\n"
        "C101,Rahul,rahul@gmail.com,Bangalore\n"
        "C102,Teja,teja@gmail.com\n"
        "C103,John,john@gmail.com,Chennai,ExtraValue\n",
        encoding="utf-8"
    )

    valid, rejected = read_csv_with_rejects(csv_file)

    # One valid record
    assert len(valid) == 1
    assert valid.iloc[0]["customer_id"] == "C101"

    # Two malformed records
    assert len(rejected) == 2

    # Check rejection reasons
    assert "Expected 4 columns, received 3 columns" in rejected.iloc[0]["reject_reason"]

    assert "Expected 4 columns, received 5 columns" in rejected.iloc[1]["reject_reason"]