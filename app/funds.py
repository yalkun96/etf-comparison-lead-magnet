"""Reviewed fund facts used by the landing page. Recheck before publication."""

CHECKED_ON = "28. 10. 2026"
EXCHANGE_SOURCE = (
    "https://www.sec.gov/Archives/edgar/data/1592900/000119312526388859/"
    "xslFormN-CEN_X05/primary_doc.xml"
)

FUNDS = [
    {
        "ticker": "STXF",
        "name": "Strive 500 ETF",
        "approach": "Široké zaměření na velké americké společnosti",
        "scope": "Velké společnosti z USA",
        "objective": (
            "Pasivně usiluje o širokou expozici vůči 500 největším veřejně "
            "obchodovaným společnostem v USA."
        ),
        "benchmark": "Bloomberg US Large Cap Index",
        "methodology": (
            "Podle aktuální stránky emitenta jde o index vážený podle "
            "kapitalizace upravené o volně obchodované akcie, který zahrnuje "
            "500 největších amerických společností."
        ),
        "expense_ratio": "0,0545 %",
        "expense_decimal": 0.000545,
        "cost_100k": "54,50 Kč",
        "issuer_url": "https://www.strivefunds.com/stxf",
        "prospectus_url": (
            "https://www.sec.gov/Archives/edgar/data/1592900/"
            "000159290025003298/ck0001592900-20251028.htm"
        ),
        "note": (
            "Prospekt z října 2025 používá název Bloomberg 500 Index. "
            "Zpráva za červen 2026 také obsahuje nekonzistentní označení. "
            "Emitent rozdíl formálně nevysvětlil; názvy zde nepovažujeme "
            "za oficiálně zaměnitelné."
        ),
    },
    {
        "ticker": "STXG",
        "name": "Strive 1000 Growth ETF",
        "approach": "Růstově orientované americké akcie",
        "scope": "Velké a střední společnosti z USA",
        "objective": (
            "Usiluje o sledování indexu amerických společností s velkou "
            "a střední kapitalizací vykazujících růstové charakteristiky, "
            "před odečtením poplatků a nákladů."
        ),
        "benchmark": "Bloomberg US 1000 Growth Index",
        "methodology": (
            "Podmnožina indexu Bloomberg US 1000. Poskytovatel indexu "
            "hodnotí tituly pomocí stejně vážených kritérií výnosnosti zisků, "
            "ocenění, dividendového výnosu a růstu."
        ),
        "expense_ratio": "0,18 %",
        "expense_decimal": 0.0018,
        "cost_100k": "180 Kč",
        "issuer_url": "https://strivefunds.com/stxg",
        "prospectus_url": (
            "https://www.sec.gov/Archives/edgar/data/1592900/"
            "000159290025003643/strive1000growthetf.htm"
        ),
        "note": "Prospekt uvádí, že index má obecně více než 500 složek.",
    },
    {
        "ticker": "STXV",
        "name": "Strive 1000 Value ETF",
        "approach": "Hodnotově orientované americké akcie",
        "scope": "Velké a střední společnosti z USA",
        "objective": (
            "Usiluje o sledování indexu amerických společností s velkou "
            "a střední kapitalizací vykazujících hodnotové charakteristiky, "
            "před odečtením poplatků a nákladů."
        ),
        "benchmark": "Bloomberg US 1000 Value Index",
        "methodology": (
            "Podmnožina indexu Bloomberg US 1000. Poskytovatel indexu "
            "hodnotí tituly pomocí stejně vážených kritérií výnosnosti zisků, "
            "ocenění, dividendového výnosu a růstu."
        ),
        "expense_ratio": "0,18 %",
        "expense_decimal": 0.0018,
        "cost_100k": "180 Kč",
        "issuer_url": "https://strivefunds.com/stxv",
        "prospectus_url": (
            "https://www.sec.gov/Archives/edgar/data/1592900/"
            "000159290025003644/strive1000valueetf.htm"
        ),
        "note": "Prospekt uvádí, že index má obecně více než 500 složek.",
    },
]

COMMON_ISSUER_NOTE = (
    "Všechny tři fondy jsou součástí EA Series Trust. Uvedené materiály "
    "identifikují jako poradce Empowered Funds, LLC (ETF Architect) "
    "a jako podporadce Strive Asset Management, LLC."
)

STXF_HISTORY_URL = (
    "https://www.sec.gov/Archives/edgar/data/1592900/"
    "000159290026004198/ck0001592900-20260630.htm"
)
STXF_TICKER_URL = (
    "https://www.sec.gov/Archives/edgar/data/1592900/"
    "000159290026002347/strivestrv-stxf497etickerc.htm"
)
STXG_SUPPLEMENT_URL = (
    "https://www.sec.gov/Archives/edgar/data/1592900/"
    "000159290026004237/strive497pmchange.htm"
)
