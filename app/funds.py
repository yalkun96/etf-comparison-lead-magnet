"""Reviewed fund facts used by the landing page. Recheck before publication."""

EXCHANGE_SOURCE = (
    "https://www.sec.gov/Archives/edgar/data/1592900/000119312526388859/"
    "xslFormN-CEN_X05/primary_doc.xml"
)
BARON_LISTING_SOURCE = (
    "https://www.sec.gov/Archives/edgar/data/2081199/000119312526196441/"
    "d121785d497.htm"
)
BROL_LISTING_SOURCE = (
    "https://www.sec.gov/Archives/edgar/data/2081199/000087666126000448/"
    "BROL052226.pdf"
)
BCSM_LISTING_SOURCE = (
    "https://www.sec.gov/Archives/edgar/data/2081199/000087666125000959/"
    "RONBBCGDBCSM121225.pdf"
)

FUNDS = [
    {
        "ticker": "STXF", "name": "Strive 500 ETF",
        "approach": "Široké zaměření na velké americké společnosti",
        "scope": "Velké společnosti z USA",
        "objective": "Pasivně usiluje o širokou expozici vůči 500 největším veřejně obchodovaným společnostem v USA.",
        "benchmark": "Bloomberg US Large Cap Index",
        "methodology": "Podle aktuální stránky emitenta jde o index vážený podle kapitalizace upravené o volně obchodované akcie, který zahrnuje 500 největších amerických společností.",
        "expense_ratio": "0,0545 %", "expense_decimal": 0.000545, "cost_100k": "54,50 Kč",
        "issuer_url": "https://www.strivefunds.com/stxf",
        "exchange_url": EXCHANGE_SOURCE,
        "prospectus_url": "https://www.sec.gov/Archives/edgar/data/1592900/000159290025003298/ck0001592900-20251028.htm",
        "source_label": "Issuer page and SEC prospectus checked 28. 10. 2026; prospectus dated 31. 10. 2025.",
        "exchange": "New York Stock Exchange, Inc.",
        "note": "The current issuer page calls the benchmark Bloomberg US Large Cap Index; the 2025 prospectus and part of the June 2026 report use Bloomberg 500 Index. The issuer has not formally reconciled these names. The ticker changed from STRV to STXF on 8 June 2026; that was not a benchmark change.",
        "preview": True,
    },
    {
        "ticker": "STXG", "name": "Strive 1000 Growth ETF",
        "approach": "Růstově orientované americké akcie",
        "scope": "Velké a střední společnosti z USA",
        "objective": "Usiluje o sledování indexu amerických společností s velkou a střední kapitalizací vykazujících růstové charakteristiky, před odečtením poplatků a nákladů.",
        "benchmark": "Bloomberg US 1000 Growth Index",
        "methodology": "Podmnožina indexu Bloomberg US 1000. Bloomberg hodnotí výnosnost zisků, ocenění, dividendový výnos a růst; skóre ovlivňují zařazení a váhy.",
        "expense_ratio": "0,18 %", "expense_decimal": 0.0018, "cost_100k": "180 Kč",
        "issuer_url": "https://strivefunds.com/stxg",
        "exchange_url": EXCHANGE_SOURCE,
        "prospectus_url": "https://www.sec.gov/Archives/edgar/data/1592900/000159290025003643/strive1000growthetf.htm",
        "source_label": "Issuer page and SEC summary prospectus checked 28. 10. 2026; prospectus dated 31. 10. 2025.",
        "exchange": "New York Stock Exchange, Inc.",
        "note": "The prospectus says the index generally has more than 500 constituents. A September 2026 supplement updates portfolio-manager information, not the researched benchmark or expense ratio.",
        "preview": True,
    },
    {
        "ticker": "STXV", "name": "Strive 1000 Value ETF",
        "approach": "Hodnotově orientované americké akcie",
        "scope": "Velké a střední společnosti z USA",
        "objective": "Usiluje o sledování indexu amerických společností s velkou a střední kapitalizací vykazujících hodnotové charakteristiky, před odečtením poplatků a nákladů.",
        "benchmark": "Bloomberg US 1000 Value Index",
        "methodology": "Podmnožina indexu Bloomberg US 1000. Bloomberg hodnotí výnosnost zisků, ocenění, dividendový výnos a růst; skóre ovlivňují zařazení a váhy.",
        "expense_ratio": "0,18 %", "expense_decimal": 0.0018, "cost_100k": "180 Kč",
        "issuer_url": "https://strivefunds.com/stxv",
        "exchange_url": EXCHANGE_SOURCE,
        "prospectus_url": "https://www.sec.gov/Archives/edgar/data/1592900/000159290025003644/strive1000valueetf.htm",
        "source_label": "Issuer page and SEC summary prospectus checked 28. 10. 2026; prospectus dated 31. 10. 2025.",
        "exchange": "New York Stock Exchange, Inc.",
        "note": "The prospectus says the index generally has more than 500 constituents. A September 2026 supplement updates portfolio-manager information, not the researched benchmark or expense ratio.",
        "preview": True,
    },
    {
        "ticker": "STXK", "name": "Strive Small-Cap ETF",
        "approach": "Malé americké společnosti",
        "scope": "Americké společnosti s malou kapitalizací",
        "objective": "Pasivně usiluje o expozici vůči 600 nejmenším společnostem podle tržní kapitalizace v indexu Bloomberg US 600 Total Return Index.",
        "benchmark": "Bloomberg US 600 Total Return Index (označení na aktuální stránce emitenta)",
        "methodology": "Výběr spodních 600 společností podle kapitalizace z Bloomberg US 1500; prospekt z října 2025 používá zkrácený název Bloomberg US 600 Index.",
        "expense_ratio": "0,18 %", "expense_decimal": 0.0018, "cost_100k": "180 Kč",
        "issuer_url": "https://strivefunds.com/stxk",
        "exchange_url": "https://strivefunds.com/stxk",
        "prospectus_url": "https://www.sec.gov/Archives/edgar/data/1592900/000159290025003645/strivesmall-capetf.htm",
        "source_label": "Issuer page and SEC summary prospectus checked 29. 10. 2026; prospectus dated 31. 10. 2025.",
        "exchange": "New York Stock Exchange, Inc.",
        "note": "The current issuer page names Bloomberg US 600 Total Return Index; the 2025 summary prospectus calls it Bloomberg US 600 Index. Both describe the fund's small-cap index approach; do not imply the names have been formally reconciled.",
        "preview": False,
    },
    {
        "ticker": "STXD", "name": "Strive 1000 Dividend Growth ETF",
        "approach": "Americké akcie s rostoucími dividendami",
        "scope": "Americké akcie s historií soustavného růstu dividend",
        "objective": "Pasivně usiluje o expozici vůči americkým akciím s historií soustavného růstu dividend.",
        "benchmark": "Bloomberg US 1000 Dividend Growth Index",
        "methodology": "Výběr zahrnuje společnosti s pěti lety růstu dividend a pětiletou mírou růstu dividend vyšší než u benchmarku.",
        "expense_ratio": "0,35 %", "expense_decimal": 0.0035, "cost_100k": "350 Kč",
        "issuer_url": "https://strivefunds.com/stxd",
        "exchange_url": "https://strivefunds.com/stxd",
        "prospectus_url": "https://www.sec.gov/Archives/edgar/data/1592900/000159290025003646/strive1000dividendgrowthetf.htm",
        "source_label": "Issuer page and SEC summary prospectus checked 29. 10. 2026; prospectus dated 31. 10. 2025.",
        "exchange": "New York Stock Exchange, Inc.",
        "note": "Issuer disclosure says the index targets U.S. equities with five consecutive years of dividend increases and a five-year dividend-growth rate greater than the benchmark.",
        "preview": False,
    },
    {
        "ticker": "DRLL", "name": "Strive U.S. Energy ETF",
        "approach": "Koncentrované zaměření na energetiku",
        "scope": "Energetický sektor USA",
        "objective": "Usiluje o sledování celkového výnosu indexu složeného z akcií kótovaných v USA v energetickém sektoru, před poplatky a náklady.",
        "benchmark": "Bloomberg US Energy Select Index",
        "methodology": "Bloomberg US Energy Select Index představuje americké akcie energetického sektoru. Prospekt uvádí, že fond přešel na tento index 11. 4. 2024.",
        "expense_ratio": "0,41 %", "expense_decimal": 0.0041, "cost_100k": "410 Kč",
        "issuer_url": "https://strivefunds.com/drll",
        "exchange_url": "https://strivefunds.com/drll",
        "prospectus_url": "https://www.sec.gov/Archives/edgar/data/1592900/000159290025003640/striveusenergyetf.htm",
        "source_label": "Strive issuer page and SEC summary prospectus checked 29. 10. 2026; prospectus dated 31. 10. 2025.",
        "exchange": "New York Stock Exchange, Inc.",
        "note": "This is concentrated sector exposure, not a broad-market substitute. The issuer page notes the benchmark changed in April 2024.",
        "preview": False,
    },
    {
        "ticker": "SHOC", "name": "Strive U.S. Semiconductor ETF",
        "approach": "Koncentrované zaměření na polovodiče",
        "scope": "Společnosti z polovodičového sektoru kótované v USA",
        "objective": "Pasivně usiluje o širokou expozici vůči polovodičovému sektoru společností kótovaných v USA.",
        "benchmark": "Bloomberg US Listed Semiconductors Select Total Return Index",
        "methodology": "Index zaměřený na polovodičové společnosti kótované v USA; issuer page uvádí změnu indexu v březnu 2024.",
        "expense_ratio": "0,40 %", "expense_decimal": 0.004, "cost_100k": "400 Kč",
        "issuer_url": "https://strivefunds.com/shoc",
        "exchange_url": "https://strivefunds.com/shoc",
        "prospectus_url": "https://www.sec.gov/Archives/edgar/data/1592900/000159290025003641/striveussemiconductoretf.htm",
        "source_label": "Strive issuer page and SEC summary prospectus checked 29. 10. 2026; prospectus dated 31. 10. 2025.",
        "exchange": "New York Stock Exchange, Inc.",
        "note": "This is concentrated sector exposure, not a broad-market substitute. The issuer page identifies the current index and the March 2024 index change.",
        "preview": False,
    },
    {
        "ticker": "BROL", "name": "Baron Risk Optimized Large Cap ETF",
        "approach": "Aktivně řízené velké růstové společnosti",
        "scope": "Velké americké společnosti; aktivní výběr a řízení rizika",
        "objective": "Usiluje o kapitálové zhodnocení a za běžných podmínek investuje převážně do akcií velkých amerických společností.",
        "benchmark": "Aktivní fond — nesleduje benchmark; S&P 500 slouží jako srovnávací index ve zprávě akcionářům.",
        "methodology": "Fundamentální výběr společností kombinovaný s kvantitativní optimalizací rizika; index není cílem kopírování.",
        "expense_ratio": "0,45 %", "expense_decimal": 0.0045, "cost_100k": "450 Kč",
        "issuer_url": "https://www.baroncapitalgroup.com/product-detail/baron-risk-optimized-large-cap-etf-brol",
        "exchange_url": BROL_LISTING_SOURCE,
        "prospectus_url": "https://www.sec.gov/Archives/edgar/data/2081199/000119312526235689/d89099d497.htm",
        "source_label": "Baron issuer page, SEC prospectus and NYSE certification checked 29. 10. 2026; fund began operations 26. 5. 2026.",
        "exchange": "New York Stock Exchange LLC.",
        "note": "The prospectus says the actively managed fund does not seek to track or replicate an index. The issuer uses the S&P 500 as a report comparator. Recent launch; limited operating history.",
        "preview": False,
    },
    {
        "ticker": "RONB", "name": "Baron First Principles ETF",
        "approach": "Aktivní růstový výběr napříč kapitalizacemi",
        "scope": "Americké růstové společnosti napříč tržními kapitalizacemi",
        "objective": "Usiluje o dlouhodobé kapitálové zhodnocení investováním do amerických růstových společností napříč kapitalizacemi.",
        "benchmark": "Russell 3000 Growth Index",
        "methodology": "Aktivní fundamentální výběr; Russell 3000 Growth slouží jako referenční index pro srovnání, fond jej nekopíruje.",
        "expense_ratio": "1,00 %", "expense_decimal": 0.01, "cost_100k": "1 000 Kč",
        "issuer_url": "https://www.baroncapitalgroup.com/product-detail/baron-first-principles-etf-ronb",
        "exchange_url": BARON_LISTING_SOURCE,
        "prospectus_url": "https://www.sec.gov/Archives/edgar/data/2081199/000119312526196441/d121785d497.htm",
        "source_label": "Baron issuer page and SEC prospectus/SAI checked 29. 10. 2026; fund began operations 12. 12. 2025.",
        "exchange": "New York Stock Exchange LLC.",
        "note": "Issuer fund summary lists Russell 3000 Growth as benchmark and 1.00% total expenses. Active, concentrated approach; do not compare as a passive index substitute.",
        "preview": False,
    },
    {
        "ticker": "BCSM", "name": "Baron SMID Cap ETF",
        "approach": "Aktivně vybírané malé a střední společnosti",
        "scope": "Americké společnosti v oblasti small- a mid-cap",
        "objective": "Usiluje o kapitálové zhodnocení prostřednictvím aktivního výběru malých a středních společností.",
        "benchmark": "Russell 2500 Growth Index; Russell 3000 je širší srovnávací index.",
        "methodology": "Aktivní výběr růstově orientovaných společností v segmentu small/mid-cap; uvedené indexy jsou referenční, nikoli fondem sledované.",
        "expense_ratio": "0,75 %", "expense_decimal": 0.0075, "cost_100k": "750 Kč",
        "issuer_url": "https://www.baroncapitalgroup.com/product-detail/baron-smid-cap-etf-bcsm",
        "exchange_url": BCSM_LISTING_SOURCE,
        "prospectus_url": "https://www.sec.gov/Archives/edgar/data/2081199/000119312526091885/d51520d485bpos.htm",
        "source_label": "Baron issuer page and SEC prospectus/SAI checked 29. 10. 2026; fund began operations 12. 12. 2025.",
        "exchange": "New York Stock Exchange LLC.",
        "note": "The SEC shareholder report compares the fund with Russell 2500 Growth and Russell 3000; active, recently launched, and not a passive index fund.",
        "preview": False,
    },
]

PREVIEW_FUNDS = [fund for fund in FUNDS if fund["preview"]]

COMMON_ISSUER_NOTE = (
    "Sedm z deseti fondů pochází z nabídky EA Series Trust, s poradcem Empowered Funds, LLC (ETF Architect) "
    "a podporadcem Strive Asset Management, LLC. Tři fondy Baron mají poradce BAMCO, Inc. Vzorek proto "
    "zahrnuje dva poskytovatele, ale stále není reprezentativním přehledem celého trhu."
)

STXF_HISTORY_URL = "https://www.sec.gov/Archives/edgar/data/1592900/000159290026004198/ck0001592900-20260630.htm"
STXF_TICKER_URL = "https://www.sec.gov/Archives/edgar/data/1592900/000159290026002347/strivestrv-stxf497etickerc.htm"
STXG_SUPPLEMENT_URL = "https://www.sec.gov/Archives/edgar/data/1592900/000159290026004237/strive497pmchange.htm"
