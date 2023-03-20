# NumcombSolver
游戏“数字蜂巢”的求解器
A solver for game numcomb

## Tutorial
1. Make sure you have Python version 3 or higher, preferably version 3.10.7.
2. Download the required Python libraries, such as scipy==1.9.3.
3. Clone https://github.com/jeffxzy/NumcombSolver.git
4. Run the command line: "python run.py"



+ test: Perform several simulation runs and obtain the average score.
+ play: Input the blocks one by one, and the program will automatically suggest and fill in the recommended position.
+ eval: Input a certain situation, and then input the blocks one by one. The program will suggest the recommended position, but you can manually fill in a different position.
+ train: Attempt to fine-tune the parameters through the minimize function.
+ bf: Attempt to fine-tune the parameters through brute force.

The input format for blocks is "456" or "4 5 6".

In particular, the input method for the wildcard block is "101010" or "10 10 10".


The code makes selections based on the evaluation score of the comb. You can change the calculation method of expscore by adjusting the x0 parameter in run.py. You can change the search depth by modifying the depth parameter in the step function in numcomb.py.