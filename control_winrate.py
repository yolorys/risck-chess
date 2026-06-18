import pandas as pd

dfs = []
for m in ['2026-02', '2026-03', '2026-04']:
    dfs.append(pd.read_csv(f'./control_checks/control_checks_{m}.csv'))

df = pd.concat(dfs, ignore_index=True)
total = len(df)

white_wins = len(df[(df['risck_player'] == 'White') & (df['result'] == '1-0')])
black_wins = len(df[(df['risck_player'] == 'Black') & (df['result'] == '0-1')])
total_wins = white_wins + black_wins
win_rate = (total_wins / total) * 100

print(f'Total Control Games: {total}')
print(f'White Check -> White Win: {white_wins}')
print(f'Black Check -> Black Win: {black_wins}')
print(f'Total Wins by Checking Player: {total_wins}')
print(f'')
print(f'--- CONTROL GROUP WIN RATE ---')
print(f'{win_rate:.2f}%')
