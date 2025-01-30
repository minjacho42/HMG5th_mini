import matplotlib.pyplot as plt
import pandas as pd
import argparse
import json

colors = ['#66b3ff', '#ff9999', '#99ff99']
# Blue, Red, Green

def visualize_sentiment_pie(comments_df, threshold):
    comments_df['label'] = comments_df['sentiment_score'].apply(
        lambda x: 'Positive' if x >= threshold else ('Neutral' if x >= -1 * threshold else 'Negative')
    )
    readers_comment_df = comments_df.groupby('reader_loyalty')['label'].value_counts(normalize=True)
    loyalty_reader = readers_comment_df['일반 독자']
    non_loyalty_reader = readers_comment_df['충성 독자']
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].pie(loyalty_reader, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 12}, labels=loyalty_reader.index, colors=colors)
    ax[1].pie(non_loyalty_reader, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 12}, labels=non_loyalty_reader.index, colors=colors)
    ax[0].set_title('Loyalty Reader')
    ax[1].set_title('Non-Loyalty Reader')
    return fig

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--threshold", type=float, required=True)
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()
    json_file_path = args.input
    with open(json_file_path, "r", encoding='utf-8') as f:
        data = json.load(f)
    comments_df = pd.DataFrame(data['comments'])
    fig = visualize_sentiment_pie(comments_df, args.threshold)
    fig.savefig(args.output)