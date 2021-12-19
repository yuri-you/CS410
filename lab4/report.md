# <center>Lab 4 </center>

<font face="楷体" size=4>

<p align="right"> 姓名：游灏溢<br/>班级：F1903302<br/>时间：3/11/2021 </p>

[toc]


## Exercise1 Adversarial Search

### Minimax Agent

In minimax agent, I construct a minimax search tree. Each depth in the search means a max layer and k min layer, which means the pacman moves 1 step and k ghosts moves 1 step perspectively.

#### Min layer

The function is to determine the action of the $ghost\_id^{th}$ ghost.

```python
def minlayer(now_gameState:GameState,layer,ghost_id):
```

And if it is the last ghost, the next layer is the max layer, otherwise is min layer of next ghost.

```python
if ghost_id==now_gameState.getNumAgents()-1:
    ...
	new_state= 
    now_gameState.generateSuccessor(ghost_id,action)
    value=maxlayer(new_state,layer+1)
else:
    ...
    new_state=
    now_gameState.generateSuccessor(ghost_id,action)
    value=minlayer(new_state,layer,ghost_id+1)
    
```

#### Max layer

The function is to determine the action of the pacman.

```python
def maxlayer(now_gameState:GameState,layer):
```

If the depth is equal to depth limitation or the game terminates, I return the value now.

```python
if layer==self.depth or now_gameState.isWin() or now_gameState.isLose():
     return self.evaluationFunction(now_gameState)
```

When the pacman is not the first layer, I need to return the best action. And when there are actions with same value, I need to randomly choose(Break tie).

 ```python
 if layer==0:
 	return random.choice(best_action)
 ```

Otherwise I only need to return the best value.

```python
else:
   	return best_value
```

#### Result

The results are different betIen two situations.

When I break ties, it will win for 40~50 percentages of time

![ex1.1.1](C:\交大\大三上\ai\lab4\figs\ex1.1.1.png)

But if I do not break ties, the percentage will rise to more than 60 percentages.

![image-20211120204828722](C:\交大\大三上\ai\lab4\figs\ex1.1.2.png)

When observating the pacman step by step,  I discover that usually the first step is ``stop`` , so the pacman will stay at the same place rather than wander around causing death.

### AlphaBeta Pruning

This method is similar to the above method. But we need to add two parameter $\alpha,\beta$.  $\alpha$ means the lower bound, $\beta$ means the upper bound. And for the max layer 

```python
if value>=beta:return value
   alpha=max(alpha,value)
```

For the min layer

```python
if value<=alpha:return value
   beta=min(beta,value)
```

Moreover, break ties cannot be applied in the alpha beta pruning because some branch may be pruned. 



### Expectimax Agent

It's the similar to the minimax agent, but it need to modify the min layer. Here min layer is the average value of all its children rather than the minimum value.

```python
for action in actions_space:
	new_state=now_gameState. 		         			generateSuccessor(ghost,action)
    average_value+=maxlayer(new_state,layer)
average_value/=len(actions_space)
```

For expectimax agent, it will win for 70-80 percentage times because the real ghost is the random ghost.

![ex1.3](C:\交大\大三上\ai\lab4\figs\ex1.3.png)

### Minimax Ghost

Design the ghost just like the minimax agent.

I still judge the deepest layer value at the max layer, for pacman. But I determine whether to return the action at the min layer, with the following

```python
if ghost==self.index and layer==0: 
	return random.choice(worst_action)
```

Here I still try to break ties.

#### Results

Here I try 4 situations

1. Minimax Pacman (with depth 4) v.s. random ghosts

2.  Expectimax Pacman (with depth 4) v.s. random ghosts
3.  Minimax Pacman (with depth 4) v.s. minimax ghosts
4.  Expectimax Pacman (with depth 4) v.s. minimax ghosts 

And test 100 times for each situation respectively, the result is below

| WinRate, AverageScores | Minimax Pacman | Expectimax Pacman |
| ---------------------- | -------------- | ----------------- |
| Random Ghost           | 0.44, -50.56   | 0.69,172.64       |
| Minimax Ghost          | 0.55,12.36     | 0.40,-78.69       |

After testing, I surprisingly find that

* When facing random ghost, expectimax stratege has better performance than minimax. While facing minimax ghost, expectimax stratege is better.
* Expectimax pacman v.s random ghost has the highest win rate and scores. Because the random ghost is not as intelligence as minimax, and the expectimax stratege is suitable for it. 
* On the contrary, the expectimax pacman v.s minimax ghost has the lowest win rate and scores, for minimax is more clever and expectimax is not suitable for it.
* When discussing why this results, in my opinion, when facing random ghost, the expectation of the ghost's actions is exactly the average, so the evaluation of state value is more accurate. The minimax agent, however, overestimated the ghost's, so the performance is not so better.


## Exercise2 Value Iteration

#### Expected_utility function

This function is used to calculate the **$Q_\pi(s,a)$** . According to the defination of MDP, 

$$ Q_\pi(s,a)=\sum_{s'\in \mathbb{S}}\limits T(s'|a)\cdot(R(s,a,s')+\gamma\cdot V(s'))$$

In this grid MDP, there are 

$$\begin{aligned}R(s,a,s')=R(s')\end{aligned}$$

So I write the function that

```python
destination=mdp.calculate_T(s,a)
value=0
for prob,x in destination:
    value+=prob*(mdp.gamma*U[x]+mdp.R(x))
return value
```

#### Best_policy function

In each iteration, I need to provide a policy based on the state value. The best policy is defined as 

$\pi(s)=argmax_{a\in \mathbb{A}} Q(s,a)$

So I code it that

```python
    max=99999
    policy=dict()	
	for s in mdp.states:
        if s in mdp.terminals:
            policy[s]=None
            continue
        value=-max
        for a in mdp.actions(s):
            now_value=expected_utility(a,s,U,mdp)
            if now_value>value:
                value=now_value
                action=a
        policy[s]=action
    return policy
```

#### Process of Value Iteration

In each iteration, I do the following steps

1. According to the state value, generate the best policy
2. According to the best policy, calculate the new state value.
3. Compare the distance of old and new value, if it is less than $\epsilon$, terminate the iteration and return the policy and state value

Here the distance I use the $\infty-$norm distance, which means

$d(V_1,V_2):=max_{i}|V_1[i]-V_2[i]|$

#### Results

1. move cost=0.01
![ex2.1](C:\交大\大三上\ai\lab4\figs\ex2.1.png)
2. move cost=0.4
![ex2.2](C:\交大\大三上\ai\lab4\figs\ex2.2.png)
3. move cost=2
![ex2.3](C:\交大\大三上\ai\lab4\figs\ex2.3.png)

## Exercise 3 Policy Iteration

#### Policy Evaluation

Here I use the iteration method to solve matrix equation

$V=\mathbb{E}_{\pi}[R+\gamma\cdot T\cdot V]$

Here I use the deterministic policy, so for each state I only need to consider one action

```python
U = {s: 0 for s in mdp.states}
for i in range(iteration_num):
	tmp_U=dict()
	for s in U:
	if s in mdp.terminals:
		tmp_U[s]=0
	else:
        tmp_U[s]=expected_utility(pi[s],s,U,mdp)
    U=tmp_U
return U
```

More to mention, the terminal states keep 0.

#### Policy Improvement

Based on the state, get the best policy.

Then comparing it to the previous judge whether the policy improved.

The process is similar to best policy function, and add

```python
return pi==policy,policy
```

#### Process of Policy Iteration

In each iteration, I do the following steps

1. According to the policy, get the state value
2. According to the  state value, improve the policy
3. Judge whether the policy changes, if not, then terminate.

You can also refer to the following figure

![PI](C:\交大\大三上\ai\lab4\figs\PI.png)![PI1](C:\交大\大三上\ai\lab4\figs\PI1.png)

#### Results

1. move cost=0.01
   ![ex3.1](C:\交大\大三上\ai\lab4\figs\ex3.1.png)
2. move cost=0.4
   ![ex3.2](C:\交大\大三上\ai\lab4\figs\ex3.2.png)
3. move cost=2
   ![ex3.3](C:\交大\大三上\ai\lab4\figs\ex3.3.png)

You can surpringly find that the value iteration and policy iteration provide the same answer, which is the best policy for those MDPs.
