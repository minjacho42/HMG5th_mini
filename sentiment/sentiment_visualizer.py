import argparse
import pandas as pd
import matplotlib.pyplot as plt


def display_total_sentiment_pie_chart(data:pd.DataFrame, threshold:float=0.6):
    """
    전체 댓글의 긍부정 평가 비율에 대한 pie chart를 보여준다.
    threshold를 기준으로 절댓값이 해당 값 이하인 commnet들은 neutral로 판별한다.

    :param data: A pandas DataFrame containing a 'label' column with sentiment scores.
    :type data: pandas.DataFrame
    :param threshold:
    :type threshold: float
    :return: None
    """
    data['sentiment'] = data['label'].apply(
        lambda x: 'Positive' if x >= threshold else ('Neutral' if x >= -1 * threshold else 'Negative')
    )

    # Calculate percentages of each sentiment
    sentiment_counts = data['sentiment'].value_counts(normalize=True) * 100

    # Plot a pie chart with the new classification
    plt.figure(figsize=(8, 8))
    plt.pie(
        sentiment_counts,
        labels=sentiment_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontsize': 12}
    )
    plt.title('Sentiment Distribution (with Neutral)', fontsize=16)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csvfile', required=True, help='Input CSV file path')
    parser.add_argument('--threshold', type=float, default=0.6, help='Threshold for positive/negative classification')
    args = parser.parse_args()
    df = pd.read_csv(args.csvfile)
    display_total_sentiment_pie_chart(df, args.threshold)