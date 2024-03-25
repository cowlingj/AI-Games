# Connect 4

Use a neural network to play connect 4

Run the following python scripts (`pipenv run python <script>`):

1. label.py (then clean.sh):
  generate (then clean) labeled data interactively by selecting the best move for a given board
2. train.py:
  train the neural network on the training data
3. test.py:
  evaluate the performance of the model using the remaining data not used for training
4. compare.py (or play.py):
  have the model play a randomly moving agent (or play against the model interactively)
