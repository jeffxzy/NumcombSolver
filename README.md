# NumcombSolver
游戏“数字蜂巢”的求解器
A solver for game numcomb

## Tutorial
1. clone
2. cd into V7-185 or W2-181 (V7 has a higher average score, W2 is more readable)
3. python run.py



+ test: Perform several simulation runs and obtain the average score.
+ play: Input the blocks one by one, and the program will automatically suggest and fill in the recommended position.
+ eval: Input a certain situation, and then input the blocks one by one. The program will suggest the recommended position, but you can manually fill in a different position.
+ train: Attempt to fine-tune the parameters through the minimize function.
+ bf: Attempt to fine-tune the parameters through brute force.

The input format for blocks is "456" or "4 5 6".

In particular, the input method for the wildcard block is "101010" or "10 10 10".