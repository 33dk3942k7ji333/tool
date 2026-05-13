import pandas as pd
import pytest

from ana_hub.app import df


def test_data_integrity():
    """測試資料集是否完整"""
    assert not df.empty
    assert "Sales" in df.columns
    assert len(df) == 8


def test_sales_values():
    """測試銷售額是否皆為正數"""
    assert (df["Sales"] > 0).all()


def test_product_types():
    """測試產品種類是否正確"""
    expected_products = ["Gadget", "Widget"]
    actual_products = df["Product"].unique().tolist()
    for p in expected_products:
        assert p in actual_products
