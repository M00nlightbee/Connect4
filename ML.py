import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from Terminal_Version.Connect4 import Connect4
from sklearn.preprocessing import StandardScaler
import joblib
import os

class MLAgent:
    def __init__(self, game=None, model_type=MLPClassifier, **model_kwargs):
        self.game = game 
        self.model_type = model_type
        self.model_kwargs = model_kwargs
        self.model = None
        self.scaler = None
        self.model_filename = f"{self.model_type.__name__}_model.pkl"
        self.scaler_filename = "scaler.pkl"
        self.load_model()

    def load_model(self):
        """Load the model and scaler if they exist, otherwise raise an error."""
        if os.path.exists(self.model_filename) and os.path.exists(self.scaler_filename):
            print(f"Loading model from {self.model_filename}...")
            self.model = joblib.load(self.model_filename)
            self.scaler = joblib.load(self.scaler_filename)
            print("Model and scaler loaded successfully.")
        else:
            print("No pre-trained model found. Please train the model first.")
            self.model = None
            self.scaler = None

    def convert_to_game_moves(self, flat_board):
        board = np.array(flat_board).reshape(6, 7)
        moves = []
        for col in range(7):
            col_vals = board[:, col]
            pieces = [val for val in col_vals if val != 0]
            for _ in pieces:
                moves.append(col)
        return moves

    def data_set_prep(self):
        columns = [f'b.{i}' for i in range(42)] + ['outcome']
        df = pd.read_csv(r'Data\connect-4.data\connect-4.data', names=columns)

        mapping = {'x': 1, 'o': -1, 'b': 0}
        df.iloc[:, :-1] = df.iloc[:, :-1].map(mapping.get)

        X_data = []
        y_data = []

        for _, row in df.iterrows():
            board_vals = row[:-1].values
            move_sequence = self.convert_to_game_moves(board_vals)
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
        return X_data, y_data

    def train_model(self, X, y):
        # Normalize the dataset
        self.scaler = StandardScaler()
        X = self.scaler.fit_transform(X)

        # Split the dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

        # Train the model
        self.model = self.model_type(**self.model_kwargs)
        print(f"Training {self.model_type.__name__} model...")
        self.model.fit(X_train, y_train)

        # Evaluate the model
        predictions = self.model.predict(X_test)
        print(f"\nTrained {self.model_type.__name__}")
        print("\nModel Accuracy:", accuracy_score(y_test, predictions) * 100, "%")
        print("Classification Report:\n", classification_report(y_test, predictions, zero_division=0))

        # Save the trained model
        joblib.dump(self.model, self.model_filename)
        joblib.dump(self.scaler, self.scaler_filename)
        print(f"Model saved as {self.model_filename}, Scaler saved as {self.scaler_filename}")

        return y_test, predictions

    def predict_move(self, board):
        if self.model is None or self.scaler is None:
            raise ValueError("Model or scaler is not loaded. Train or load the model first.")
        board_arr = np.array(board).reshape(1, -1)
        board_arr = self.scaler.transform(board_arr)  # Scale the input
        predicted_move = int(round(self.model.predict(board_arr)[0]))
        return max(0, min(6, predicted_move))

    def choose_move(self, game, player=1):
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
        predicted_move = self.predict_move(input_features)

        # Ensure the predicted move is valid
        if predicted_move in available_cols:
            return predicted_move
        else:
            # Default to a random valid move if the prediction is invalid
            return np.random.choice(available_cols) if available_cols else None

def play_game(agent):
    game = Connect4()
    current_player = 1
    player_map = {1: "●", -1: "○"}

    while True:
        game.display_board()
        available_cols = game.get_available_moves(game.board)
        print(f"Available columns: {available_cols}")

        if current_player == 1:
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
            print("AI's move:")
            col = agent.choose_move(game, player=-1)
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

        current_player *= -1

if __name__ == "__main__":
    try:
        agent = MLAgent()
        X, y = agent.data_set_prep()
        y_test, predictions = agent.train_model(X, y)
        if y_test is not None and predictions is not None:
            # Visualization
            plt.figure(figsize=(8, 6))
            plt.scatter(y_test, predictions, edgecolor='black', alpha=0.7, color='plum', label='Predicted Moves')
            z = np.polyfit(y_test, predictions, 1)
            p = np.poly1d(z)
            plt.plot(y_test, p(y_test), color='red', linewidth=2, label='Regression Line')
            plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], linestyle='--', color='green', linewidth=2, label='Perfect Prediction')
            plt.xlabel('Actual Next Move (y_test)', fontsize=12, weight='bold')
            plt.ylabel('Predicted Next Move (predictions)', fontsize=12, weight='bold')
            plt.title('Actual vs Predicted Moves in Connect 4', fontsize=14, weight='bold')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.4)
            plt.show()

        play_game(agent)
    except Exception as e:
        print(f"An error occurred: {e}")
