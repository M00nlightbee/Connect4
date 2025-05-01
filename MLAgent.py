import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from Terminal_Version.Connect4 import Connect4
from sklearn.preprocessing import StandardScaler
import joblib
import os

def convert_to_game_moves(flat_board):
    board = np.array(flat_board).reshape(6, 7)
    moves = []
    for col in range(7):
        col_vals = board[:, col]
        pieces = [val for val in col_vals if val != 0]
        for _ in pieces:
            moves.append(col)
    return moves

def data_set_prep():
    columns = [f'b.{i}' for i in range(42)] + ['outcome']
    df = pd.read_csv(r'Data\connect-4.data\connect-4.data', names=columns)

    mapping = {'x': 1, 'o': -1, 'b': 0}
    df.iloc[:, :-1] = df.iloc[:, :-1].map(mapping.get)

    X_data = []
    y_data = []

    for _, row in df.iterrows():
        board_vals = row[:-1].values
        move_sequence = convert_to_game_moves(board_vals)
        game = Connect4()
        player_map = {1: "●", -1: "○"}
        player_turns = [1 if i % 2 == 0 else -1 for i in range(len(move_sequence))]

        for i, (move, player_id) in enumerate(zip(move_sequence[:-1], player_turns[:-1])):
            flat_numeric_board = np.where(game.board == "●", 1,
                                  np.where(game.board == "○", -1, 0)).flatten()
            turn_count = np.count_nonzero(flat_numeric_board)
            X_data.append(np.append(flat_numeric_board, turn_count))
            y_data.append(move_sequence[i + 1])  # Next move is the target
            game.make_move(move, player_map[player_id])

    X_data = np.array(X_data)
    y_data = np.array(y_data)

    print("Dataset built:")
    print(f"Total training samples: {X_data.shape[0]}")
    # print("Inferred move for that board:", y_data[0])
    return X_data, y_data


def train_model(X, y, model_type=SVC, **model_kwargs):
    # Normalize the dataset
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
    model = model_type(**model_kwargs)
    print(f"Training {model_type.__name__} model...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    print(f"\nTrained {model_type.__name__}")
    print("\nModel Accuracy:", accuracy_score(y_test, predictions) * 100, "%")
    print("Classification Report:\n", classification_report(y_test, predictions, zero_division=0))

    # Save the trained model
    model_filename = f"{model_type.__name__}_model.pkl"
    joblib.dump(model, model_filename)
    print(f"Model saved as {model_filename}")

    return model

# def train_model(X, y, model_type=SVC, **model_kwargs):
#     # Define the model filename
#     model_filename = f"{model_type.__name__}_model.pkl"

#     # Check if the model file already exists
#     if os.path.exists(model_filename):
#         print(f"Model file {model_filename} already exists. Loading the model...")
#         model = joblib.load(model_filename)
#         print(f"Model loaded from {model_filename}")
#         return model

#     # Normalize the dataset
#     scaler = StandardScaler()
#     X = scaler.fit_transform(X)

#     # Split the dataset
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

#     # Train the model
#     model = model_type(**model_kwargs)
#     print(f"Training {model_type.__name__} model...")
#     model.fit(X_train, y_train)

#     # Evaluate the model
#     predictions = model.predict(X_test)
#     print(f"\nTrained {model_type.__name__}")
#     print("\nModel Accuracy:", accuracy_score(y_test, predictions) * 100, "%")
#     print("Classification Report:\n", classification_report(y_test, predictions, zero_division=0))

#     # Save the trained model
#     joblib.dump(model, model_filename)
#     print(f"Model saved as {model_filename}")

#     return model

def predict_move(board, model):
    board_arr = np.array(board).reshape(1, -1)
    predicted_move = int(round(model.predict(board_arr)[0]))
    return max(0, min(6, predicted_move))

def choose_move(game, model, player=1):
    opponent = -player
    player_map = {1: "●", -1: "○"}
    opponent_symbol = player_map[opponent]
    available_cols = game.get_available_moves(game.board)

    # Check if the AI can block the opponent's winning move
    for col in available_cols:
        temp_board = game.drop_piece(game.board.copy(), col, opponent_symbol)
        if temp_board is not None and game.check_winner(opponent_symbol, temp_board):
            return col  # Block opponent's winning move

    # Use the trained model to predict the next move
    flat_board = np.where(game.board == "●", 1,
                          np.where(game.board == "○", -1, 0)).flatten()
    turn_count = np.count_nonzero(flat_board)
    input_features = np.append(flat_board, turn_count)

    # Predict the move using the trained model
    predicted_move = predict_move(input_features, model)

    # Ensure the predicted move is valid
    if predicted_move in available_cols:
        return predicted_move
    else:
        # Default to a random valid move if the prediction is invalid
        return np.random.choice(available_cols) if available_cols else None

def play_game(model):
    game = Connect4()
    current_player = 1
    player_map = {1: "●", -1: "○"}

    while True:
        game.display_board()
        available_cols = game.get_available_moves(game.board)
        print(f"Available columns: {available_cols}")

        if current_player == 1:
            # Human player move
            while True:
                try:
                    col = int(input("Enter column (0-6): "))
                    if col in available_cols:
                        game.make_move(col, player_map[current_player])
                        break
                    else:
                        print("Column full or invalid.")
                except ValueError:
                    print("Invalid input.")
        else:
            # AI move
            print("AI's move:")
            col = choose_move(game, model, player=-1)
            if col is not None:
                print(f"AI chooses column {col}")
                game.make_move(col, player_map[current_player])
            else:
                print("AI could not make a move!")
                break

        if game.check_winner("○"):
            game.display_board()
            print("AI wins!")
            break
        elif game.check_winner("●"):
            game.display_board()
            print("You win!")
            break
        elif game.is_full(game.board):
            game.display_board()
            print("It's a draw!")
            break

        # Switch player
        current_player *= -1

if __name__ == "__main__":
    try:
        X, y = data_set_prep()
        X, y = X[:100000], y[:100000]  # Use only the first 100,000 samples
        model_choice = input("Choose model (logistic, forest, svc, lsvc): ").strip().lower()
        
        if model_choice == "forest":
            model = train_model(X, y, model_type=RandomForestClassifier, n_estimators=100)
        elif model_choice == "svc":
            model = train_model(X, y, model_type=SVC, kernel='linear')
        elif model_choice == "lsvc":
            from sklearn.svm import LinearSVC
            model = train_model(X, y, model_type=LinearSVC)
        else:
            model = train_model(X, y, model_type=LogisticRegression)
        
        print("Model training completed.")
        play_game(model)
    except Exception as e:
        print(f"An error occurred: {e}")




# # Visualization

# plt.figure(figsize=(8, 6))

# # # Scatter plot: Actual vs Predicted moves
# plt.scatter(y_test, predictions, edgecolor='black', alpha=0.7, color='plum', label='Predicted Moves')

# # Regression line (best fit) through predicted vs actual moves
# z = np.polyfit(y_test, predictions, 1)  # Linear fit (degree=1)
# p = np.poly1d(z)
# plt.plot(y_test, p(y_test), color='red', linewidth=2, label='Regression Line')

# # Perfect prediction line (y=x)
# plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], linestyle='--', color='green', linewidth=2, label='Perfect Prediction')

# # Labels and Title
# plt.xlabel('Actual Next Move (y_test)', fontsize=12, weight='bold')
# plt.ylabel('Predicted Next Move (predictions)', fontsize=12, weight='bold')
# plt.title('Actual vs Predicted Moves in Connect 4', fontsize=14, weight='bold')

# plt.legend()
# plt.grid(True, linestyle='--', alpha=0.4)
# plt.show()