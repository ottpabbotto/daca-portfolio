import pandas as pd


# ============================================================
# 1. ANDMETE PUHASTAMINE
# ============================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Puhastab müügiandmed.

    Tegevused:
        1. Kontrollib vajalike veergude olemasolu.
        2. Eemaldab duplikaadid invoice_id põhjal.
        3. Eemaldab read, kus puudub customer_id,
           sale_date või total_price.
        4. Teisendab sale_date datetime formaati.
        5. Eemaldab read, mille kuupäeva teisendamine ebaõnnestus.

    Args:
        df: Müügiandmete DataFrame.

    Returns:
        Puhastatud DataFrame.
    """

    required_columns = [
        "invoice_id",
        "customer_id",
        "sale_date",
        "total_price"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Müügiandmetest puuduvad vajalikud veerud: "
            f"{missing_columns}"
        )

    # Teeme koopia, et vältida algse DataFrame'i muutmist.
    df_clean = df.copy()

    # --------------------------------------------------------
    # 1. Duplikaatide eemaldamine
    # --------------------------------------------------------

    df_clean = df_clean.drop_duplicates(
        subset=["invoice_id"],
        keep="first"
    )

    # --------------------------------------------------------
    # 2. Kriitiliste NULL väärtuste eemaldamine
    # --------------------------------------------------------

    df_clean = df_clean.dropna(
        subset=[
            "customer_id",
            "sale_date",
            "total_price"
        ]
    )

    # --------------------------------------------------------
    # 3. Kuupäeva teisendamine
    # --------------------------------------------------------

    df_clean["sale_date"] = pd.to_datetime(
        df_clean["sale_date"],
        errors="coerce"
    )

    # Eemaldame read, mille kuupäeva teisendamine ebaõnnestus.
    df_clean = df_clean.dropna(
        subset=["sale_date"]
    )

    return df_clean


# ============================================================
# 2. NÄDALANE AGREGATSIOON
# ============================================================

def calculate_weekly_aggregates(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Koondab müügiandmed nädalate kaupa.

    Arvutatavad näitajad:
        - revenue
        - order_count
        - avg_order_value

    Args:
        df: Puhastatud müügiandmete DataFrame.

    Returns:
        Nädalate kaupa agregeeritud DataFrame.
    """

    required_columns = [
        "sale_date",
        "total_price",
        "invoice_id"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Nädalase agregeerimise jaoks puuduvad veerud: "
            f"{missing_columns}"
        )

    if df.empty:
        return pd.DataFrame(
            columns=[
                "revenue",
                "order_count",
                "avg_order_value"
            ]
        )

    # Veendume, et kuupäev oleks datetime tüüpi.
    df = df.copy()

    df["sale_date"] = pd.to_datetime(
        df["sale_date"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["sale_date"]
    )

    weekly = (
        df
        .resample(
            "W",
            on="sale_date"
        )
        .agg(
            revenue=("total_price", "sum"),
            order_count=("invoice_id", "nunique"),
            avg_order_value=("total_price", "mean")
        )
    )

    return weekly


# ============================================================
# 3. KPI-DE ARVUTAMINE
# ============================================================

def calculate_kpis(
    df: pd.DataFrame
) -> dict:
    """
    Arvutab põhilised müügi KPI-d.

    KPI-d:
        - total_revenue
        - unique_customers
        - avg_order_value

    Args:
        df: Puhastatud müügiandmete DataFrame.

    Returns:
        Dictionary KPI väärtustega.
    """

    required_columns = [
        "total_price",
        "customer_id"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "KPI-de arvutamiseks puuduvad veerud: "
            f"{missing_columns}"
        )

    if df.empty:
        return {
            "total_revenue": 0.0,
            "unique_customers": 0,
            "avg_order_value": 0.0
        }

    total_revenue = df["total_price"].sum()
    unique_customers = df["customer_id"].nunique()
    avg_order_value = df["total_price"].mean()

    return {
        "total_revenue": round(
            float(total_revenue),
            2
        ),
        "unique_customers": int(
            unique_customers
        ),
        "avg_order_value": round(
            float(avg_order_value),
            2
        )
    }


# ============================================================
# 4. ANDMESETTIDE ÜHENDAMINE
# ============================================================

def merge_datasets(
    df_sales: pd.DataFrame,
    df_customers: pd.DataFrame
) -> pd.DataFrame:
    """
    Liidab müügi- ja kliendiandmed customer_id põhjal.

    Kasutab LEFT JOIN-i, et säilitada kõik müügitehingud.

    Args:
        df_sales: Müügiandmete DataFrame.
        df_customers: Kliendiandmete DataFrame.

    Returns:
        Müügi- ja kliendiandmeid sisaldav DataFrame.
    """

    if "customer_id" not in df_sales.columns:
        raise ValueError(
            "Müügiandmetes puudub customer_id."
        )

    if "customer_id" not in df_customers.columns:
        raise ValueError(
            "Kliendiandmetes puudub customer_id."
        )

    return pd.merge(
        df_sales,
        df_customers,
        on="customer_id",
        how="left"
    )


# ============================================================
# 5. KVALITEEDITESTID
# ============================================================

def run_quality_tests() -> None:
    """
    Käivitab transform.py kvaliteeditestid näidisandmetega.

    Testib:
        - clean_data()
        - calculate_kpis()
        - calculate_weekly_aggregates()
        - merge_datasets()

    Testid käivitatakse ainult siis, kui transform.py
    käivitatakse otse. Importimisel neid ei käivitata.
    """

    print("=" * 60)
    print("TRANSFORM.PY KVALITEEDITESTID")
    print("=" * 60)

    # --------------------------------------------------------
    # Näidisandmed
    # --------------------------------------------------------

    # Andmed sisaldavad:
    # - invoice_id 2 on duplikaat
    # - üks customer_id on NULL
    # - kõik vajalikud veerud on olemas

    sales_raw = {
        "invoice_id": [
            1,
            2,
            2,
            3,
            4
        ],
        "customer_id": [
            101,
            102,
            102,
            103,
            None
        ],
        "sale_date": [
            "2025-01-01",
            "2025-01-02",
            "2025-01-02",
            "2025-01-10",
            "2025-01-11"
        ],
        "total_price": [
            100.0,
            50.0,
            50.0,
            150.0,
            20.0
        ]
    }

    customers_raw = {
        "customer_id": [
            101,
            102,
            103
        ],
        "name": [
            "Tiina",
            "Kevin",
            "Mati"
        ]
    }

    df_sales_raw = pd.DataFrame(
        sales_raw
    )

    df_customers_raw = pd.DataFrame(
        customers_raw
    )

    # --------------------------------------------------------
    # TEST 1: clean_data()
    # --------------------------------------------------------

    print("\n[TEST 1] clean_data()")

    df_cleaned = clean_data(
        df_sales_raw
    )

    expected_rows = 3

    if len(df_cleaned) == expected_rows:
        print(
            f"[PASS] Ridade arv: {len(df_cleaned)} "
            f"(ootuspärane: {expected_rows})"
        )
    else:
        print(
            f"[FAIL] Ridade arv: {len(df_cleaned)} "
            f"(ootuspärane: {expected_rows})"
        )

    # Kontrollime, et invoice_id duplikaate poleks.
    duplicate_count = (
        df_cleaned["invoice_id"]
        .duplicated()
        .sum()
    )

    if duplicate_count == 0:
        print(
            "[PASS] invoice_id duplikaadid on eemaldatud."
        )
    else:
        print(
            "[FAIL] invoice_id duplikaadid on alles."
        )

    # Kontrollime, et customer_id NULL väärtusi poleks.
    null_customers = (
        df_cleaned["customer_id"]
        .isna()
        .sum()
    )

    if null_customers == 0:
        print(
            "[PASS] Kriitilised NULL väärtused on eemaldatud."
        )
    else:
        print(
            "[FAIL] customer_id sisaldab NULL väärtusi."
        )

    # Kontrollime kuupäeva tüüpi.
    if pd.api.types.is_datetime64_any_dtype(
        df_cleaned["sale_date"]
    ):
        print(
            "[PASS] sale_date on datetime formaadis."
        )
    else:
        print(
            "[FAIL] sale_date ei ole datetime formaadis."
        )

    # --------------------------------------------------------
    # TEST 2: calculate_kpis()
    # --------------------------------------------------------

    print("\n[TEST 2] calculate_kpis()")

    kpis = calculate_kpis(
        df_cleaned
    )

    print(
        f"[INFO] KPI-d: {kpis}"
    )

    expected_revenue = 300.0
    expected_customers = 3
    expected_avg = 100.0

    if kpis["total_revenue"] == expected_revenue:
        print(
            "[PASS] Total revenue on korrektne."
        )
    else:
        print(
            f"[FAIL] Total revenue: "
            f"{kpis['total_revenue']} "
            f"(ootuspärane: {expected_revenue})"
        )

    if kpis["unique_customers"] == expected_customers:
        print(
            "[PASS] Unikaalsete klientide arv on korrektne."
        )
    else:
        print(
            f"[FAIL] Klientide arv: "
            f"{kpis['unique_customers']} "
            f"(ootuspärane: {expected_customers})"
        )

    if kpis["avg_order_value"] == expected_avg:
        print(
            "[PASS] Keskmine ostukorvi väärtus on korrektne."
        )
    else:
        print(
            f"[FAIL] Keskmine väärtus: "
            f"{kpis['avg_order_value']} "
            f"(ootuspärane: {expected_avg})"
        )

    # --------------------------------------------------------
    # TEST 3: calculate_weekly_aggregates()
    # --------------------------------------------------------

    print(
        "\n[TEST 3] calculate_weekly_aggregates()"
    )

    weekly = calculate_weekly_aggregates(
        df_cleaned
    )

    if not weekly.empty:
        print(
            "[PASS] Nädalane agregatsioon sisaldab andmeid."
        )
        print(weekly)
    else:
        print(
            "[FAIL] Nädalane agregatsioon on tühi."
        )

    # --------------------------------------------------------
    # TEST 4: merge_datasets()
    # --------------------------------------------------------

    print("\n[TEST 4] merge_datasets()")

    df_merged = merge_datasets(
        df_cleaned,
        df_customers_raw
    )

    if not df_merged.empty:
        print(
            "[PASS] Andmestikud ühendati."
        )
    else:
        print(
            "[FAIL] Ühendatud DataFrame on tühi."
        )

    # Kontrollime esimest klienti.
    first_customer = df_merged.iloc[0]["name"]

    if first_customer == "Tiina":
        print(
            "[PASS] Esimese müügi klient on Tiina."
        )
    else:
        print(
            f"[FAIL] Esimese müügi klient: "
            f"{first_customer} "
            f"(ootuspärane: Tiina)"
        )

    print("\n" + "=" * 60)
    print("KVALITEEDITESTID LÕPETATUD")
    print("=" * 60)


# ============================================================
# 6. OTSE KÄIVITAMINE
# ============================================================

if __name__ == "__main__":
    run_quality_tests()