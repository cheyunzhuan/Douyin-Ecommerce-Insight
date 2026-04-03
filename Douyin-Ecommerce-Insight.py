import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 设置绘图风格 ---
sns.set(style="whitegrid")
# 移除了中文字体设置，使用默认的英文字体，确保不乱码
# plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False


class DouyinDataAnalyzer:
    def __init__(self):
        self.data = None
        self.cleaned_data = None

    # 1. 模拟数据生成
    def generate_mock_data(self, rows=1000):
        print("🚀 Generating mock data...")
        np.random.seed(42)

        # 模拟流量来源 (改为英文)
        sources = np.random.choice(
            ['Feed Rec', 'Search', 'Live Stream', 'Short Video', 'Other'],
            rows,
            p=[0.4, 0.2, 0.2, 0.15, 0.05]
        )
        # 模拟曝光量 (100 - 5000)
        impressions = np.random.randint(100, 5000, rows)
        # 模拟点击率 (1% - 10%)
        ctr = np.random.uniform(0.01, 0.10, rows)
        # 计算点击量
        clicks = (impressions * ctr).astype(int)

        # 模拟转化数据
        conversion_rate = np.random.uniform(0.01, 0.05, rows)
        conversions = (clicks * conversion_rate).astype(int)

        # 模拟GMV
        gmv = np.random.normal(500, 200, rows)
        gmv = np.clip(gmv, 50, 2000)  # 限制范围

        # 创建 DataFrame
        self.data = pd.DataFrame({
            'source': sources,
            'impressions': impressions,
            'ctr': ctr,
            'clicks': clicks,
            'conversion_rate': conversion_rate,
            'conversions': conversions,
            'gmv': gmv
        })
        print("✅ 数据生成完成。")
        return self.data

    # 2. 数据清洗
    def clean_data(self):
        if self.data is None:
            print("❌ 错误：请先生成数据。")
            return None

        print("🧹 正在清洗数据...")
        # 简单的去重和空值处理
        self.cleaned_data = self.data.dropna().drop_duplicates()
        print(f"✅ 数据清洗完成。剩余行数: {len(self.cleaned_data)}")
        return self.cleaned_data

    # 3. 绘制图表 (已全部改为英文标签)
    def plot_analysis(self):
        if self.cleaned_data is None:
            print("❌ 错误：请先清洗数据。")
            return

        print("🎨 正在绘制分析图表...")

        # 创建 2x2 的画布
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Douyin Traffic Source Analysis Dashboard', fontsize=20, y=0.98)

        # --- 图表 1: 流量来源占比 (饼图) ---
        # 修正点：使用 axes[0, 0]
        source_counts = self.cleaned_data['source'].value_counts()
        axes[0, 0].pie(
            source_counts,
            labels=source_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=sns.color_palette("Pastel1")
        )
        axes[0, 0].set_title('Traffic Source Distribution', fontsize=14)

        # --- 图表 2: 各来源平均点击率 (柱状图) ---
        # 修正点：使用 axes[0, 1]
        ctr_by_source = self.cleaned_data.groupby('source')['ctr'].mean().sort_values(ascending=False)
        sns.barplot(
            x=ctr_by_source.index,
            y=ctr_by_source.values,
            ax=axes[0, 1],
            palette="viridis"
        )
        axes[0, 1].set_title('Average CTR by Source', fontsize=14)
        axes[0, 1].set_ylabel('CTR')
        axes[0, 1].set_xlabel('Source')
        axes[0, 1].tick_params(axis='x', rotation=45)

        # --- 图表 3: 曝光量 vs 点击率 (散点图) ---
        # 修正点：使用 axes[1, 0]
        sns.scatterplot(
            data=self.cleaned_data,
            x='impressions',
            y='ctr',
            hue='source',
            ax=axes[1, 0],
            alpha=0.6,
            palette="deep"
        )
        axes[1, 0].set_title('Impressions vs CTR', fontsize=14)
        axes[1, 0].set_xlabel('Impressions')
        axes[1, 0].set_ylabel('CTR')
        # 调整图例位置防止遮挡
        axes[1, 0].legend(title='Source', loc='upper right')

        # --- 图表 4: 各来源GMV总和 (折线图) ---
        # 修正点：使用 axes[1, 1]
        gmv_by_source = self.cleaned_data.groupby('source')['gmv'].sum()
        axes[1, 1].plot(
            gmv_by_source.index,
            gmv_by_source.values,
            marker='o',
            linewidth=2,
            color='red',
            markersize=8
        )
        axes[1, 1].set_title('Total GMV by Source', fontsize=14)
        axes[1, 1].set_ylabel('Total GMV ($)')
        axes[1, 1].set_xlabel('Source')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, linestyle='--', alpha=0.7)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()
        print("✅ 图表绘制完成。")

    # 主流程控制
    def run(self):
        self.generate_mock_data()
        self.clean_data()
        self.plot_analysis()


# --- 运行程序 ---
if __name__ == "__main__":
    analyzer = DouyinDataAnalyzer()
    analyzer.run()