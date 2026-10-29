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
        "source_label": "Stránka emitenta a prospekt SEC kontrolovány 28. 10. 2026; prospekt je datován 31. 10. 2025.",
        "exchange": "New York Stock Exchange, Inc.",
        "note": "Aktuální stránka emitenta označuje benchmark jako Bloomberg US Large Cap Index; prospekt z roku 2025 a část zprávy z června 2026 používají název Bloomberg 500 Index. Emitent tento rozdíl formálně nevysvětlil. Ticker se změnil ze STRV na STXF dne 8. 6. 2026; nešlo o změnu benchmarku.",
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
        "source_label": "Stránka emitenta a zkrácený prospekt SEC kontrolovány 28. 10. 2026; prospekt je datován 31. 10. 2025.",
        "exchange": "New York Stock Exchange, Inc.",
        "note": "Prospekt uvádí, že index obvykle zahrnuje více než 500 složek. Dodatek ze září 2026 aktualizuje informace o správcích portfolia, nikoli zde uvedený benchmark nebo sazbu nákladů.",
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
        "source_label": "Stránka emitenta a zkrácený prospekt SEC kontrolovány 28. 10. 2026; prospekt je datován 31. 10. 2025.",
        "exchange": "New York Stock Exchange, Inc.",
        "note": "Prospekt uvádí, že index obvykle zahrnuje více než 500 složek. Dodatek ze září 2026 aktualizuje informace o správcích portfolia, nikoli zde uvedený benchmark nebo sazbu nákladů.",
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
        "source_label": "Stránka emitenta a zkrácený prospekt SEC kontrolovány 29. 10. 2026; prospekt je datován 31. 10. 2025.",
        "exchange": "New York Stock Exchange, Inc.",
        "note": "Aktuální stránka emitenta uvádí Bloomberg US 600 Total Return Index; zkrácený prospekt z roku 2025 používá název Bloomberg US 600 Index. Oba dokumenty popisují indexový přístup fondu zaměřený na malé společnosti; názvy nepovažujte za formálně sjednocené.",
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
        "source_label": "Stránka emitenta a zkrácený prospekt SEC kontrolovány 29. 10. 2026; prospekt je datován 31. 10. 2025.",
        "exchange": "New York Stock Exchange, Inc.",
        "note": "Informace emitenta uvádějí, že index vybírá americké akcie s pěti po sobě jdoucími roky růstu dividend a s pětiletou mírou růstu dividend vyšší než u benchmarku.",
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
        "source_label": "Stránka emitenta Strive a zkrácený prospekt SEC kontrolovány 29. 10. 2026; prospekt je datován 31. 10. 2025.",
        "exchange": "New York Stock Exchange, Inc.",
        "note": "Jde o koncentrovanou sektorovou expozici, nikoli náhradu širokého trhu. Stránka emitenta uvádí změnu benchmarku v dubnu 2024.",
        "preview": False,
    },
    {
        "ticker": "SHOC", "name": "Strive U.S. Semiconductor ETF",
        "approach": "Koncentrované zaměření na polovodiče",
        "scope": "Společnosti z polovodičového sektoru kótované v USA",
        "objective": "Pasivně usiluje o širokou expozici vůči polovodičovému sektoru společností kótovaných v USA.",
        "benchmark": "Bloomberg US Listed Semiconductors Select Total Return Index",
        "methodology": "Index zaměřený na polovodičové společnosti kótované v USA; stránka emitenta uvádí, že se sledovaný index změnil v březnu 2024.",
        "expense_ratio": "0,40 %", "expense_decimal": 0.004, "cost_100k": "400 Kč",
        "issuer_url": "https://strivefunds.com/shoc",
        "exchange_url": "https://strivefunds.com/shoc",
        "prospectus_url": "https://www.sec.gov/Archives/edgar/data/1592900/000159290025003641/striveussemiconductoretf.htm",
        "source_label": "Stránka emitenta Strive a zkrácený prospekt SEC kontrolovány 29. 10. 2026; prospekt je datován 31. 10. 2025.",
        "exchange": "New York Stock Exchange, Inc.",
        "note": "Jde o koncentrovanou sektorovou expozici, nikoli náhradu širokého trhu. Stránka emitenta uvádí aktuální index a jeho změnu v březnu 2024.",
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
        "source_label": "Stránka emitenta Baron, prospekt SEC a potvrzení NYSE kontrolovány 29. 10. 2026; fond zahájil činnost 26. 5. 2026.",
        "exchange": "New York Stock Exchange LLC.",
        "note": "Prospekt uvádí, že aktivně řízený fond neusiluje o sledování ani kopírování indexu. Emitent používá S&P 500 jako srovnávací index ve zprávě. Fond byl založen nedávno a má krátkou provozní historii.",
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
        "source_label": "Stránka emitenta Baron a prospekt/informace SAI SEC kontrolovány 29. 10. 2026; fond zahájil činnost 12. 12. 2025.",
        "exchange": "New York Stock Exchange LLC.",
        "note": "Souhrn fondu od emitenta uvádí Russell 3000 Growth jako benchmark a celkové náklady 1,00 %. Jde o aktivní a koncentrovaný přístup; fond nelze chápat jako náhradu pasivního indexového fondu.",
        "preview": False,
    },
    {
        "ticker": "BCSM", "name": "Baron SMID Cap ETF",
        "approach": "Aktivně vybírané malé a střední společnosti",
        "scope": "Americké společnosti s malou a střední tržní kapitalizací",
        "objective": "Usiluje o kapitálové zhodnocení prostřednictvím aktivního výběru malých a středních společností.",
        "benchmark": "Russell 2500 Growth Index; Russell 3000 je širší srovnávací index.",
        "methodology": "Aktivní výběr růstově orientovaných společností s malou a střední tržní kapitalizací; uvedené indexy jsou referenční, nikoli fondem sledované.",
        "expense_ratio": "0,75 %", "expense_decimal": 0.0075, "cost_100k": "750 Kč",
        "issuer_url": "https://www.baroncapitalgroup.com/product-detail/baron-smid-cap-etf-bcsm",
        "exchange_url": BCSM_LISTING_SOURCE,
        "prospectus_url": "https://www.sec.gov/Archives/edgar/data/2081199/000119312526091885/d51520d485bpos.htm",
        "source_label": "Stránka emitenta Baron a prospekt/informace SAI SEC kontrolovány 29. 10. 2026; fond zahájil činnost 12. 12. 2025.",
        "exchange": "New York Stock Exchange LLC.",
        "note": "Zpráva akcionářům SEC srovnává fond s Russell 2500 Growth a Russell 3000; jde o aktivně řízený fond s krátkou historií, nikoli o pasivní indexový fond.",
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
