import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from snownlp import SnowNLP
import matplotlib

matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
matplotlib.rcParams['axes.unicode_minus'] = False
FONT_PATH = 'msyh.ttc'
INPUT_CSV = "C:/Users/33240/Downloads/jd_comment_data.xlsx"

def load_data(file):
    df = pd.read_excel(file)

    print("列名：", df.columns.tolist())

    df = df.rename(columns={
        '评分（总分5分）(score)': 'score',
        '评价内容(content)': 'comment'
    })

    if 'score' not in df.columns or 'comment' not in df.columns:
        raise ValueError("数据文件中必须包含 'score' 和 'comment' 两列（或对应的中文字段）")

    df = df.dropna(subset=['score', 'comment'])
    df['score'] = df['score'].astype(int)
    df = df.sample(n=1000, random_state=42)
    return df

def draw_score_histogram(df):
    plt.figure(figsize=(6, 4))
    df['score'].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.xlabel("评分（1-5星）")
    plt.ylabel("评论数")
    plt.title("用户评分分布直方图")
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def generate_wordcloud(df):
    text = " ".join(df['comment'].astype(str))
    seg_text = " ".join(jieba.cut(text))
    wc = WordCloud(font_path=FONT_PATH, background_color='white',
                   width=800, height=600, max_words=200).generate(seg_text)

    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title("评论词云图")
    plt.show()

def sentiment_analysis(df):
    print("正在进行情感分析（可能需要几秒）...")
    df['sentiment'] = df['comment'].astype(str).apply(lambda x: SnowNLP(x).sentiments)
    avg_sentiment = df.groupby('score')['sentiment'].mean()

    plt.figure(figsize=(6, 4))
    plt.plot(avg_sentiment.index, avg_sentiment.values, marker='o', linestyle='-', color='orange')
    plt.title("用户评分与情感分析折线图")
    plt.xlabel("评分（1-5星）")
    plt.ylabel("平均情感得分（0~1）")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    try:
        df = load_data(INPUT_CSV)
        draw_score_histogram(df)
        generate_wordcloud(df)
        sentiment_analysis(df)
    except Exception as e:
        print("发生错误：", e)

if __name__ == "__main__":
    main()
