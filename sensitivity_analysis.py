import os
import subprocess
import re
import csv

# Configuration: Target dataset and threshold permutations
DATA_YEAR = "2026"
DATA_MONTH = "04"

permutations = [
    (5, 400),
    (10, 400),
    (15, 400),
    (15, 200),
    (15, 300)
]

sql_template = """INSTALL aixchess FROM community;
LOAD aixchess;

COPY (
    WITH exploded_games AS (
        SELECT 
            lichess_id,
            result,
            UNNEST(range(2, length(evals) + 1)) AS ply,
            evals,
            clocks_white,
            clocks_black,
            move_details(movedata) AS moves
        FROM './data/aix_lichess_{YEAR}-{MONTH}_low.parquet'
        WHERE 
            time_increment = 0 
            AND time_initial IN (60, 180)
            AND length(evals) >= 2
    )
    SELECT 
        lichess_id,
        ply,
        result,
        CASE WHEN ply % 2 = 1 THEN 'White' ELSE 'Black' END AS risck_player,
        [m."from" || m."to" || m.promotion FOR m IN moves] AS move_list
    FROM exploded_games
    WHERE 
        moves[ply].is_check = TRUE
        AND (
            CASE 
                WHEN ply % 2 = 1 THEN clocks_black[CAST(floor(ply / 2.0) AS INTEGER)] 
                ELSE clocks_white[CAST(floor(ply / 2.0) AS INTEGER)]
            END
        ) <= {T_O}
        AND (
            CASE 
                WHEN ply % 2 = 1 THEN eval_to_centipawns(evals[ply]) - eval_to_centipawns(evals[ply - 1])
                ELSE (eval_to_centipawns(evals[ply]) - eval_to_centipawns(evals[ply - 1])) * -1
            END
        ) <= -{DELTA_E}
) TO './candidate_riscks/candidate_riscks_pilot.csv' (HEADER, DELIMITER ',');
"""

with open("./results/sensitivity_analysis_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["T_O", "Delta_E", "Win_Rate", "Reaction_Time", "N"])

for to, de in permutations:
    print(f"\n============================")
    print(f"Running Permutation T_O={to}, Delta_E={de}")
    print(f"============================")
    
    sql_query = sql_template.format(T_O=to, DELTA_E=de, YEAR=DATA_YEAR, MONTH=DATA_MONTH)
    sql_file = f"./phase1_filter/phase1_filter_T{to}_E{de}.sql"
    with open(sql_file, "w") as f:
        f.write(sql_query)
        
    print("Running Phase 1 (DuckDB)...")
    subprocess.run(["./duckdb", "-unsigned", "-c", f".read {sql_file}"], check=True)
    
    print("Running Phase 2 (risck_filter.py)...")
    subprocess.run(["python", "risck_filter.py", "pilot"], check=True)
    
    print("Running Phase 3 (Win Rate & Reaction Time)...")
    wr_out = subprocess.run(["python", "risck_winrate.py", "pilot"], capture_output=True, text=True, check=True).stdout
    ro_out = subprocess.run(["python", "risck_opponent_reaction.py", "pilot"], capture_output=True, text=True, check=True).stdout
    
    wr_match = re.search(r"--- GLOBAL WIN RATE \(W_SC\) ---\n([\d.]+)%", wr_out)
    win_rate = wr_match.group(1) if wr_match else "N/A"
    
    n_match = re.search(r"Total True RISCKs analyzed: (\d+)", wr_out)
    n_count = n_match.group(1) if n_match else "N/A"
    
    ro_match = re.search(r"--- AVERAGE REACTION TIME \(R_O\) ---\n([\d.]+) seconds", ro_out)
    ro = ro_match.group(1) if ro_match else "N/A"
    
    with open("./results/sensitivity_analysis_results.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([to, de, win_rate, ro, n_count])
        
    print(f"Results: Win Rate {win_rate}%, R_O {ro}s, N {n_count}")

print("\nOrchestration complete!")
