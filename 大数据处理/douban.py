import requests,re
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

headers = {
    'User-Agent': 'Mozilla/5.0'
}

def fetch_movies(num_pages=4):
    movies = []
    for i in range(num_pages):
        url = f"https://movie.douban.com/top250?start={i * 25}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='item')

        for item in items:
            try:
                title = item.find('span', class_='title').text.strip()
                rating = float(item.find('span', class_='rating_num').text.strip())

                people_text = item.find('div', class_='bd').find_all('span')[-1].text
                people_match = re.search(r'(\d+)', people_text.replace(',', ''))
                people = int(people_match.group(1)) if people_match else 0

                info = item.find('div', class_='bd').p.get_text(strip=True)
                director_match = re.search(r'导演:\s*([^/]+)', info)
                director = director_match.group(1).strip() if director_match else "未知"

                year_match = re.search(r'(\d{4})', info)
                year = int(year_match.group(1)) if year_match else 0

                movies.append({
                    'title': title,
                    'rating': rating,
                    'people': people,
                    'director': director,
                    'year': year,
                })
            except Exception as e:
                print(f"跳过一条，错误：{e}")
                continue
    return movies

def save_png():
    df = pd.read_excel('豆瓣电影数据.xlsx', engine='openpyxl').head(10)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 图1：电影评分对比
    df_rating_sorted = df.sort_values(by='rating', ascending=False)
    plt.figure(figsize=(10, 6))
    bars = plt.barh(df_rating_sorted['title'], df_rating_sorted['rating'], color='lightblue')
    plt.title('电影评分对比')
    plt.xlabel('评分')
    plt.ylabel('电影名称')
    plt.gca().invert_yaxis()
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.05, bar.get_y() + bar.get_height() / 2,
                f'{width:.1f}', va='center')
    plt.tight_layout()
    plt.savefig('电影评分对比.png', dpi=300)
    plt.show()
    # 图2：评分随年份变化趋势
    df_sorted = df.sort_values(by='year')
    plt.figure(figsize=(8, 5))
    plt.plot(df_sorted['year'], df_sorted['rating'], marker='o', linestyle='-', color='dodgerblue')
    plt.title('评分随年份变化趋势')
    plt.xlabel('年份')
    plt.ylabel('评分')
    plt.grid(True)
    for x, y in zip(df_sorted['year'], df_sorted['rating']):
        plt.text(x, y + 0.05, str(x), ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig('评分随年份变化趋势.png', dpi=300)
    plt.show()
    # 图3：导演对应电影评分
    def clean_director(d):
        if pd.isna(d):
            return ''
        before_actor = d.split('主演')[0].strip()
        chinese_match = re.findall(r'[\u4e00-\u9fa5·]{2,}', before_actor)
        if chinese_match:
            return chinese_match[0]
        english_match = re.findall(r'[A-Za-z\s\.\-]+', before_actor)
        if english_match:
            return english_match[0].strip()
        return before_actor
    df['director_clean'] = df['director'].apply(clean_director)
    plt.figure(figsize=(10, 6))
    bars2 = plt.bar(df['director_clean'], df['rating'], color='lightseagreen')
    plt.title('导演对应电影评分')
    plt.xlabel('导演')
    plt.ylabel('评分')
    plt.xticks(rotation=45, ha='right')
    for bar in bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.05,
                f'{height:.1f}', ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig('导演对应电影评分.png', dpi=300)
    plt.show()
    # 图4：电影观看人数占比
    plt.figure(figsize=(7, 7))
    labels = [f"{title}\n人数: {people}" for title, people in zip(df['title'], df['people'])]
    plt.pie(df['people'], labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('电影观看人数占比')
    plt.tight_layout()
    plt.savefig('电影观看人数占比.png', dpi=300)
    plt.show()

def main():
    print("开始抓取豆瓣电影 Top 100...")
    movies = fetch_movies(num_pages=4)
    df = pd.DataFrame(movies)
    df.to_excel("豆瓣电影数据.xlsx", index=False)
    print("数据已保存到 Excel 文件：豆瓣电影数据.xlsx")
    save_png()

if __name__ == "__main__":
    main()
