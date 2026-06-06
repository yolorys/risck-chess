import pandas as pd
import chess

print("Starting Phase 2: Full Dataset Geometric RISCK Filter...")

# 1. Load the Phase 1 Pilot Data
df = pd.read_csv('spite_checks_pilot.csv')
total_spite_checks = len(df)
print(f"Loaded {total_spite_checks} potential spite checks. Processing...")

true_riscks = []
error_count = 0

# 2. Iterate over the FULL dataset
for index, row in df.iterrows():
    
    # Print a progress update every 10,000 rows
    if index > 0 and index % 10000 == 0:
        print(f"Processed {index}/{total_spite_checks} rows... Found {len(true_riscks)} RISCKs so far.")
        
    game_id = row['lichess_id']
    target_ply = int(row['ply'])

    try:
        moves_list = [move.strip() for move in row['move_list'].strip("[]").split(",")]
        board = chess.Board()
        
        for i in range(target_ply):
            board.push_uci(moves_list[i])
            
        # --- THE GEOMETRIC FILTER ---
        last_move = board.peek()
        attacker_sq = last_move.to_square
        king_sq = board.king(board.turn)
        
        is_adjacent = chess.square_distance(king_sq, attacker_sq) <= 1
        is_capturable = any(legal_move.to_square == attacker_sq for legal_move in board.legal_moves)
        piece_type = board.piece_at(attacker_sq).piece_type
        is_major_piece = piece_type != chess.PAWN
        
        if is_adjacent and is_capturable and is_major_piece:
            true_riscks.append(row)
            
    except ValueError as e:
        error_count += 1
        continue

# 3. Save the final refined dataset
final_df = pd.DataFrame(true_riscks)
if not final_df.empty:
    final_df = final_df.drop(columns=['move_list'])
final_df.to_csv('true_riscks_dataset.csv', index=False)

print(f"\nPhase 2 Complete!")
print(f"Found {len(true_riscks)} True RISCKs out of {total_spite_checks} total candidates.")
if error_count > 0:
    print(f"Note: {error_count} games were skipped due to PGN/UCI parsing errors.")
print("Saved to 'true_riscks_dataset.csv'.")
