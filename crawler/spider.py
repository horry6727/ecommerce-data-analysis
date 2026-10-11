import os
import csv
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

# ================= 配置区 =================
BASE_URL = "https://books.toscrape.com/"
LIST_URL = "https://books.toscrape.com/catalogue/category/books_1/page-{page}.html"
OUTPUT_PATH = "data/raw/dataproducts.csv"  # 规范化的原始数据存放路径

# 星级文本 → 数字映射表
RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}


def scrape_page(page_obj, limit=None):
    """从当前页提取商品列表（含评分）"""
    items = page_obj.locator("article.product_pod")
    count = items.count()
    print(f"  📦 本页找到 {count} 个商品")

    products = []
    for i in range(count):
        item = items.nth(i)

        # --- 提取标题 & URL ---
        title_el = item.locator("h3 a")
        title = title_el.inner_text().strip() if title_el.count() else "未知标题"
        href = title_el.get_attribute("href") or ""
        url_full = urljoin(BASE_URL, href)

        # --- 提取价格 ---
        price_el = item.locator(".price_color")
        price = price_el.inner_text().strip() if price_el.count() else ""

        # --- 提取评分（核心新增逻辑）---
        rating = 0
        rating_el = item.locator("p.star-rating")
        if rating_el.count():
            class_attr = rating_el.get_attribute("class") or ""
            # class 格式: "star-rating Three" → 取最后一个单词
            rating_word = class_attr.strip().split()[-1]
            rating = RATING_MAP.get(rating_word, 0)

        product = {
            "title": title,
            "price": price,
            "rating": rating,
            "url": url_full,
        }
        products.append(product)

        if limit and len(products) >= limit:
            break

    return products


def save_to_csv(data):
    """将商品列表保存为 CSV 文件"""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # 覆盖写入，避免追加导致表头重复
    fieldnames = ["title", "price", "rating", "url"]

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"\n✅ CSV 已保存: {OUTPUT_PATH}")
    print(f"   共写入 {len(data)} 条记录（含 rating 字段）")


def scrape_products(max_pages=3, per_page_limit=None):
    """主采集流程：翻页 + 保存"""
    all_products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for i in range(1, max_pages + 1):
            url = BASE_URL if i == 1 else LIST_URL.format(page=i)
            print(f"\n🔍 正在采集第 {i}/{max_pages} 页: {url}")

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
            except Exception as e:
                print(f"  ❌ 页面加载失败: {e}")
                break

            products = scrape_page(page, limit=per_page_limit)
            all_products.extend(products)

            if not products:
                print("  ⚠️ 本页无商品，停止翻页")
                break

        browser.close()

    save_to_csv(all_products)
    return all_products


if __name__ == "__main__":
    data = scrape_products(max_pages=3, per_page_limit=20)
    print(f"\n🎉 采集完成，共获取 {len(data)} 个商品")