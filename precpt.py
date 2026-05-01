import numpy as np

class Perceptron:
    def __init__(self, learning_rate=0.01, n_iters=1000):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.activation_func = self._unit_step_func
        self.weights = None
        self.bias = None

    def _unit_step_func(self, x):
        return np.where(x >= 0, 1, 0)

    def fit(self, X, y):
        n_samples, n_features = X.shape

        # Step 1: Initialize parameters
        self.weights = np.zeros(n_features)
        self.bias = 0

        y_ = np.array([1 if i > 0 else 0 for i in y])

        # Step 2: Training loop
        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                # Linear combination
                linear_output = np.dot(x_i, self.weights) + self.bias
                # Apply activation function
                y_predicted = self.activation_func(linear_output)

                # Step 3: Perceptron update rule
                update = self.lr * (y_[idx] - y_predicted)
                self.weights += update * x_i
                self.bias += update

    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        y_predicted = self.activation_func(linear_output)
        return y_predicted

# Example Usage: Training on a logical AND gate
if __name__ == "__main__":
    # Input data (X) and Labels (y)
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([0, 0, 0, 1]) 

    p = Perceptron(learning_rate=0.1, n_iters=10)
    p.fit(X, y)

    print("Weights:", p.weights)
    print("Bias:", p.bias)
    print("Predictions:", p.predict(X))
