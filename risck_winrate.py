import pandas as pd

print("Calculating Global Win Rate (W_SC)...")

# 1. Load the finalized RISCK dataset
df = pd.read_csv('true_riscks_dataset.csv')
total_riscks = len(df)

if total_riscks == 0:
    print("Dataset is empty. No RISCKs to analyze.")
    exit()

# 2. Filter for games where the player who executed the RISCK actually won
# '1-0' means White won, '0-1' means Black won
white_wins = df[(df['spite_check_player'] == 'White') & (df['result'] == '1-0')]
black_wins = df[(df['spite_check_player'] == 'Black') & (df['result'] == '0-1')]

total_wins = len(white_wins) + len(black_wins)

# 3. Calculate the percentage
win_rate = (total_wins / total_riscks) * 100

print(f"Total True RISCKs analyzed: {total_riscks}")
print(f"Total games WON after executing a RISCK: {total_wins}")
print(f"\n--- GLOBAL WIN RATE (W_SC) ---")
print(f"{win_rate:.2f}%\n")
