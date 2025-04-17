from TradingPack.Database.connection import conn
from TradingPack.DataScraping.SectorIndustry import ScrapingSectorIndustry

cursor = conn.cursor()

# Bring Sectors
cursor.execute("SELECT Id, Name, Url FROM Sector")
sectors = cursor.fetchall()

# Collect and save sectors data
for sector in sectors:
    sector_id, sector_name, sector_url = sector
    print(f"📡 Scraping: {sector_name}")
    try:
        ScrapingSectorIndustry("Sector", sector_id, sector_name, sector_url)
    except Exception as e:
        print(f"❌ Error with {sector_name}: {e}")