import logging
import time

import data_fetcher
import transform
import visualize_export


# Seadistame logimise nii faili kui ka konsooli.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)


def run_pipeline():
    """
    Käivitab UrbanStyle'i andmetöötluse kõik etapid järjekorras.

    Pipeline koosneb neljast põhietapist:
        1. Andmete hankimine
        2. Andmete puhastamine ja liitmine
        3. Andmete agregeerimine
        4. Visualiseerimine ja tulemuste eksport

    Tagastab:
        bool:
            True, kui pipeline läbis kõik etapid edukalt.
            False, kui mõnes etapis tekkis viga.
    """
    logging.info("Pipeline käivitatud.")

    try:
        # ETAPP 1: FETCH
        # Hangime müügi- ja kliendiandmed Supabase'ist.
        logging.info("Etapp 1: Andmete hankimine Supabase'ist.")

        df_sales = data_fetcher.fetch_sales(
            start_date="2024-01-01",
            end_date="2024-12-31"
        )

        df_customers = data_fetcher.fetch_customers()

        logging.info(
            f"Andmete hankimine edukas: laeti {len(df_sales)} müügirida."
        )

        # ETAPP 2: CLEAN & MERGE
        # Liidame müügi- ja kliendiandmed ning puhastame tulemuse.
        logging.info("Etapp 2: Andmete puhastamine ja liitmine.")

        df_merged = transform.merge_datasets(
            df_sales,
            df_customers
        )

        df_clean = transform.clean_data(df_merged)

        logging.info(
            "Andmete puhastamine ja liitmine edukalt lõpetatud."
        )

        # ETAPP 3: AGGREGATE
        logging.info(
            "Etapp 3: Nädalaste koondnäitajate ja KPI-de arvutamine."
        )

        df_weekly = transform.calculate_weekly_aggregates(df_clean)

        print("\nNädalase koondtabeli veerud:")
        print(df_weekly.columns.tolist())

        print("\nNädalase koondtabeli esimesed read:")
        print(df_weekly.head())

        kpis = transform.calculate_kpis(df_clean)

        logging.info("Agregeerimine edukalt lõpetatud.")

        # ETAPP 4: VISUALIZE & EXPORT
        # Loome diagrammid ja salvestame tulemused output-kausta.
        logging.info(
            "Etapp 4: Visualiseerimine ja tulemuste eksport."
        )

        fig_weekly = visualize_export.create_weekly_chart(df_weekly)
        fig_kpi = visualize_export.create_kpi_summary(kpis)

        output_dir = "output"

        visualize_export.export_results(
            df_weekly,
            output_dir,
            figs=[fig_weekly, fig_kpi]
        )

        logging.info(
            f"Pipeline edukalt lõpetatud. "
            f"Tulemused asuvad kaustas: {output_dir}"
        )

        return True

    except Exception as e:
        # Logime vea koos veateatega, et probleemi oleks lihtsam tuvastada.
        logging.error(
            f"Pipeline katkestati vea tõttu: {str(e)}"
        )

        return False


if __name__ == "__main__":
    """
    Käivitab pipeline'i ja mõõdab kogu protsessi tööaega.
    """

    # Salvestame pipeline'i algusaja.
    start_time = time.time()

    # Käivitame kogu andmetöötluse pipeline'i.
    success = run_pipeline()

    # Arvutame pipeline'i kogukestuse sekundites.
    elapsed_time = time.time() - start_time

    # Kuvame kasutajale lõpptulemuse.
    if success:
        print(
            f"\nKOKKUVÕTE: Pipeline läbis kõik etapid "
            f"{round(elapsed_time, 2)} sekundiga."
        )
    else:
        print(
            "\nKOKKUVÕTE: Pipeline ebaõnnestus. "
            "Vaata detaile pipeline.log failist."
        )