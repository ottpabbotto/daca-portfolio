import os

import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client


# ============================================================
# 1. KESKKONNA MUUTUJATE LAADIMINE
# ============================================================

load_dotenv()

url: str | None = os.getenv("SUPABASE_URL")
key: str | None = os.getenv("SUPABASE_KEY")


# ============================================================
# 2. KONFIGURATSIOONI KONTROLL
# ============================================================

if not url:
    raise ValueError(
        "SUPABASE_URL puudub .env failis. "
        "Kontrolli, et .env fail asuks projekti juurkaustas "
        "ja sisaldaks SUPABASE_URL väärtust."
    )

if not key:
    raise ValueError(
        "SUPABASE_KEY puudub .env failis. "
        "Kontrolli, et .env fail sisaldaks SUPABASE_KEY väärtust."
    )


# ============================================================
# 3. SUPABASE ÜHENDUSE LOOMINE
# ============================================================

try:
    supabase: Client = create_client(
        url,
        key
    )

except Exception as e:
    raise ConnectionError(
        "Supabase ühenduse loomine ebaõnnestus. "
        "Kontrolli SUPABASE_URL ja SUPABASE_KEY väärtusi. "
        f"Viga: {e}"
    ) from e


# ============================================================
# 4. MÜÜGIANDMETE HANKIMINE
# ============================================================

def fetch_sales(
    start_date: str,
    end_date: str
) -> pd.DataFrame:
    """
    Hangib Supabase'i sales tabelist müügiandmed
    määratud kuupäevavahemikus.

    Kuupäevafilter rakendatakse Supabase API tasemel,
    et vältida kogu tabeli allalaadimist.

    Args:
        start_date:
            Perioodi alguskuupäev formaadis YYYY-MM-DD.

        end_date:
            Perioodi lõppkuupäev formaadis YYYY-MM-DD.

    Returns:
        Müügiandmeid sisaldav pandas DataFrame.

        Kui päring ebaõnnestub, tagastatakse tühi
        DataFrame ja väljastatakse veateade.
    """

    try:
        response = (
            supabase
            .table("sales")
            .select("*")
            .gte(
                "sale_date",
                start_date
            )
            .lte(
                "sale_date",
                end_date
            )
            .execute()
        )

        df = pd.DataFrame(
            response.data
        )

        if df.empty:
            print(
                "HOIATUS: müügiandmeid ei leitud "
                f"perioodil {start_date} kuni {end_date}."
            )
        else:
            print(
                f"Müügiandmed hangitud: "
                f"{len(df)} rida."
            )

        return df

    except Exception as e:
        print(
            "VIGA: müügiandmete hankimine ebaõnnestus. "
            "Kontrolli Supabase'i ühendust, API võtit "
            f"ja tabeli õigusi. Detailid: {e}"
        )

        return pd.DataFrame()


# ============================================================
# 5. KLIENDIANDMETE HANKIMINE
# ============================================================

def fetch_customers() -> pd.DataFrame:
    """
    Hangib Supabase'i customers tabelist kõik kliendiandmed.

    Funktsioon ei kasuta kuupäevafiltrit, sest kliendiandmeid
    kasutatakse müügiandmete täiendamiseks customer_id põhjal.

    Returns:
        Kõiki kliente sisaldav pandas DataFrame.

        Kui päring ebaõnnestub, tagastatakse tühi DataFrame
        ja väljastatakse veateade.
    """

    try:
        response = (
            supabase
            .table("customers")
            .select("*")
            .execute()
        )

        df = pd.DataFrame(
            response.data
        )

        if df.empty:
            print(
                "HOIATUS: customers tabelist "
                "ei leitud andmeid."
            )
        else:
            print(
                f"Kliendiandmed hangitud: "
                f"{len(df)} rida."
            )

        return df

    except Exception as e:
        print(
            "VIGA: kliendiandmete hankimine ebaõnnestus. "
            "Kontrolli Supabase'i ühendust, API võtit "
            f"ja tabeli õigusi. Detailid: {e}"
        )

        return pd.DataFrame()


# ============================================================
# 6. TOOTEANDMETE HANKIMINE
# ============================================================

def fetch_products() -> pd.DataFrame:
    """
    Hangib Supabase'i products tabelist kõik tooteandmed.

    Toodete andmeid kasutatakse hiljem analüüsis,
    visualiseerimisel või müügiandmetega ühendamisel.

    Returns:
        Kõiki tooteid sisaldav pandas DataFrame.

        Kui päring ebaõnnestub, tagastatakse tühi DataFrame
        ja väljastatakse veateade.
    """

    try:
        response = (
            supabase
            .table("products")
            .select("*")
            .execute()
        )

        df = pd.DataFrame(
            response.data
        )

        if df.empty:
            print(
                "HOIATUS: products tabelist "
                "ei leitud andmeid."
            )
        else:
            print(
                f"Tooteandmed hangitud: "
                f"{len(df)} rida."
            )

        return df

    except Exception as e:
        print(
            "VIGA: tooteandmete hankimine ebaõnnestus. "
            "Kontrolli Supabase'i ühendust, API võtit "
            f"ja tabeli õigusi. Detailid: {e}"
        )

        return pd.DataFrame()


# ============================================================
# 7. KVALITEEDI- JA ÜHENDUSTEST
# ============================================================

def run_fetch_tests() -> None:
    """
    Käivitab fetch_data.py testid.

    Testid kontrollivad:
        - Supabase ühenduse toimimist
        - müügiandmete hankimist
        - kliendiandmete hankimist
        - tooteandmete hankimist

    Funktsiooni kasutatakse arenduse ja kvaliteedikontrolli
    ajal.

    Kui fetch_data.py imporditakse pipeline.py-sse,
    teste automaatselt ei käivitata.
    """

    print("=" * 60)
    print("FETCH_DATA.PY KVALITEEDITESTID")
    print("=" * 60)

    # --------------------------------------------------------
    # Testperiood müügiandmete jaoks
    # --------------------------------------------------------

    start_date = "2024-01-01"
    end_date = "2024-01-31"

    print(
        f"\nTestperiood: "
        f"{start_date} kuni {end_date}"
    )

    # --------------------------------------------------------
    # Müügiandmed
    # --------------------------------------------------------

    print("\n[TEST 1] fetch_sales()")

    df_sales = fetch_sales(
        start_date,
        end_date
    )

    if isinstance(df_sales, pd.DataFrame):
        print(
            "[PASS] fetch_sales() tagastas DataFrame'i."
        )

        if not df_sales.empty:
            print(
                f"[PASS] Müügiandmeid leiti: "
                f"{len(df_sales)} rida."
            )
            print(
                "\nEsimesed read:"
            )
            print(
                df_sales.head()
            )
        else:
            print(
                "[WARN] fetch_sales() tagastas "
                "tühja DataFrame'i."
            )

    else:
        print(
            "[FAIL] fetch_sales() ei tagastanud "
            "DataFrame'i."
        )

    # --------------------------------------------------------
    # Kliendiandmed
    # --------------------------------------------------------

    print("\n[TEST 2] fetch_customers()")

    df_customers = fetch_customers()

    if isinstance(
        df_customers,
        pd.DataFrame
    ):
        print(
            "[PASS] fetch_customers() "
            "tagastas DataFrame'i."
        )

        if not df_customers.empty:
            print(
                f"[PASS] Kliendiandmeid leiti: "
                f"{len(df_customers)} rida."
            )
            print(
                "\nEsimesed read:"
            )
            print(
                df_customers.head()
            )
        else:
            print(
                "[WARN] fetch_customers() "
                "tagastas tühja DataFrame'i."
            )

    else:
        print(
            "[FAIL] fetch_customers() ei tagastanud "
            "DataFrame'i."
        )

    # --------------------------------------------------------
    # Tooteandmed
    # --------------------------------------------------------

    print("\n[TEST 3] fetch_products()")

    df_products = fetch_products()

    if isinstance(
        df_products,
        pd.DataFrame
    ):
        print(
            "[PASS] fetch_products() "
            "tagastas DataFrame'i."
        )

        if not df_products.empty:
            print(
                f"[PASS] Tooteandmeid leiti: "
                f"{len(df_products)} rida."
            )
            print(
                "\nEsimesed read:"
            )
            print(
                df_products.head()
            )
        else:
            print(
                "[WARN] fetch_products() "
                "tagastas tühja DataFrame'i."
            )

    else:
        print(
            "[FAIL] fetch_products() ei tagastanud "
            "DataFrame'i."
        )

    print("\n" + "=" * 60)
    print("FETCH_DATA.PY TESTID LÕPETATUD")
    print("=" * 60)


# ============================================================
# 8. OTSE KÄIVITAMINE
# ============================================================

if __name__ == "__main__":
    run_fetch_tests()