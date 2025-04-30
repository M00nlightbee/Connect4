import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, classification_report
from Terminal_Version.Connect4 import Connect4  # Adjust the import to match the folder structure

# def dataset():   
#     # Load the dataset 
#     df = pd.read_csv(r'Data\connect-4.data\connect-4.data', header=None)

#     # Output info
#     print("\nShape of the dataset:", df.shape)
#     print("\nFirst 5 rows:\n", df.head())
#     print("\nData types:\n", df.dtypes)
#     print("\nMissing values in each column:\n", df.isnull().sum())
#     print(df.info())
#     print(df.describe())

#     return df

# if __name__ == "__main__":
#     dataset()

# def preprocess_data():

#     columns = [f'b.{i}' for i in range(42)] + ['outcome']
#     # Load the dataset 
#     df = pd.read_csv(r'Data\connect-4.data\connect-4.data', names=columns)
    
#     # Mapping numeric values
#     mapping = {'x': 1, 'o': -1, 'b': 0}
#     encoded_df = df.copy() 
#     encoded_df.iloc[:, :-1] = encoded_df.iloc[:, :-1].map(mapping.get)

#     print("Shape of encoded_df:", encoded_df.shape)
#     print(encoded_df.head())

def convert_to_game_moves(flat_board):
    board = np.array(flat_board).reshape(6, 7)
    moves = []
    for col in range(7):
        col_vals = board[:, col]
        pieces = [val for val in col_vals if val != 0]
        for _ in pieces:
            moves.append(col)
    return moves

def build_state_action_dataset():
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
    print("Example board:", X_data[0])
    print("Inferred move for that board:", y_data[0])
    return X_data, y_data

def split_dataset(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, shuffle=True
    )

    print("Train set:", X_train.shape, y_train.shape)
    print("Test set:", X_test.shape, y_test.shape)

    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Build the dataset
    X, y = build_state_action_dataset()

    # Split the dataset
    X_train, X_test, y_train, y_test = split_dataset(X, y)

model = LinearRegression()

model.fit(X_train, y_train)
print(model.intercept_)

# Create a DataFrame for coefficients
coeff_df = pd.DataFrame(model.coef_, columns=['Coefficient'])

# Print the coefficients
print(coeff_df)

# Predict the next moves
predictions = model.predict(X_test)

plt.figure(figsize=(8, 6))

# Scatter plot: Actual vs Predicted moves
plt.scatter(y_test, predictions, edgecolor='black', alpha=0.7, color='plum', label='Predicted Moves')

# Regression line (best fit) through predicted vs actual moves
z = np.polyfit(y_test, predictions, 1)  # Linear fit (degree=1)
p = np.poly1d(z)
plt.plot(y_test, p(y_test), color='red', linewidth=2, label='Regression Line')

# Perfect prediction line (y=x)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], linestyle='--', color='green', linewidth=2, label='Perfect Prediction')

# Labels and Title
plt.xlabel('Actual Next Move (y_test)', fontsize=12, weight='bold')
plt.ylabel('Predicted Next Move (predictions)', fontsize=12, weight='bold')
plt.title('Actual vs Predicted Moves in Connect 4', fontsize=14, weight='bold')

plt.legend()
plt.grid(True, linestyle='--', alpha=0.4)
plt.show()


