import pandas as pd

def load_data(deliveries_path, matches_path):
    deliveries = pd.read_csv(deliveries_path)
    matches = pd.read_csv(matches_path)
    df = deliveries.merge(matches, left_on='match_id', right_on='id')
    df.fillna(0, inplace=True)
    return df

def get_phase(over):
    if 0 <= over <= 6:
        return 'Powerplay'
    elif 7 <= over <= 15:
        return 'Middle'
    elif 16 <= over <= 20:
        return 'Death'
    return 'Unknown'

def process_batter_stats(df):
    df['phase'] = df['over'].apply(get_phase)
    
    stats = df.groupby(['batter', 'phase']).agg(
        runs=('batsman_runs', 'sum'),
        balls_faced=('ball', 'count'),
        dismissals=('is_wicket', 'sum'),
        fours=('batsman_runs', lambda x: (x == 4).sum()),
        sixes=('batsman_runs', lambda x: (x == 6).sum())
    ).reset_index()
    
    stats['strike_rate'] = (stats['runs'] / stats['balls_faced']) * 100
    
    pivot = stats.pivot(index='batter', columns='phase', values=[
        'runs', 'balls_faced', 'dismissals', 'fours', 'sixes', 'strike_rate'
    ])
    
    pivot.columns = ['{}_{}'.format(metric, phase) for metric, phase in pivot.columns]
    pivot = pivot.reset_index().fillna(0)
    
    return pivot

def score_batters(df, phase, w_sr=0.6, w_runs=0.4):
    sr_col = f"strike_rate_{phase}"
    runs_col = f"runs_{phase}"
    df["score"] = (df[sr_col] * w_sr) + (df[runs_col] * w_runs)
    return df.sort_values("score", ascending=False)
