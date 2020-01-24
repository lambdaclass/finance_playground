The emergence of cooperation in evolutionary systems
====================================================
<br />
Notes for Peters and Adamou (2018) [_An evolutionary advantage of cooperation_](https://arxiv.org/abs/1506.03414)

This paper tackles the apparently paradoxical emergence of cooperation patterns under evolutionary dynamics.  
Why do we observe seemingly _altruistic_ behavior in systems where organisms compete for resources and only the fittest thrive (the so called _survival of the fittest_)?   
Classical solutions propose a net fitness gain from collaboration. The authors seek to explain this gain through the analysis of the time-average growth rate for the fitness of the collaborating organisms.

Consider a species in their transition from single cell to multicellular organisms. This change occurs when cells agglomerate and begin sharing nutrients through common membranes, increasing their biomass. Entities with more biomass come to dominate the environment and generate more of themselves.  

The paper proposes the following dynamics for the system:
- entities gain biomass according to an [Itô diffusion](https://en.wikipedia.org/wiki/Itô_diffusion) process, where the change in biomass for entity $x_i$ is:

$$d x_i = x_i(\mu dt + \sigma d \mathit{W_i})$$

where $\mu$ is the drift, $\sigma$ the volatility and $\mathit{W_i}$ is a [Wiener process](https://en.wikipedia.org/wiki/Wiener_process).
- the growth rate over time $T$ is defined as

$$g(x_i, T) \equiv \frac{1}{T} \ln{\Big( \frac{x_i(T)}{x_i(0)} \Big)}$$

## Cooperation protocol
<br />
The baseline model consists of $N$ non-cooperating entities $x_i$. This system is compared to one where a  mutation is introduced that hardwires cooperation into the entities. The _cooperators_, hence referred to as $y_i$, pool resources and then share them equally.

The growth phase is the same for all entities in both systems (cooperators and non-cooperators)

$$ \Delta x_i(t) = x_i(t)(\mu \Delta t + \sigma \xi_i \sqrt{\Delta t})$$

where $\xi_i$ are iid variates with $\xi_{i} \sim \mathcal{N}(0,1)$

Then there is a cooperating phase, and the cooperators' biomass at time $t + \Delta t$ is given by

$$ y_{i}(t+\Delta t)=\frac{1}{N} \sum_{j=1}^{N}\left(y_{j}(t)+\Delta y_{j}(t)\right)=y_{i}(t)+\frac{1}{N} \sum_{j=1}^{N} \Delta y_{j}(t) $$



## Analysis of the system
<br />
From the point of view of ensamble averaging, given identical initial biomasses $x_i(0) = y_i(0)$ we have

$$\left\langle x_{i}(t)\right\rangle = \left\langle y_{i}(t)\right\rangle = x_{i}(0) \exp (\mu t)$$

Moreover, in a cooperating pair, the entity with higher initial biomass could increase its expectation value by breaking off the cooperation.  

The answer to the paradox comes when the system is viewed from the time-averaging perspective. The authors show that non-cooperators grow at 

$$\overline{g}\left(x_{i}\right)=\mu-\sigma^{2} / 2$$

whereas cooperators grow at

$$\overline{g}\left(y^{(N)}\right)=\mu-\frac{\sigma^{2}}{2 N}$$

where

\begin{equation}
\overline{g}\left(y^{(N)}\right)-\overline{g}\left(x_{i}\right)=\frac{\sigma^{2}}{2}\left(1-\frac{1}{N}\right) \\
\overline{g}\left(y^{(N)}\right) > \overline{g}\left(x_{i}\right) ,\, N > 1
\end{equation}

## Plots
<br />
Figure 2 from Peters' and Adamou's paper shows the expectation value and growth rate for non colaborating and for $N = 2$ colaborating entities.
<label for="imgemergence-of-cooperation_11_0" class="margin-toggle">⊕</label>
<input type="checkbox" id="imgemergence-of-cooperation_11_0" class="margin-toggle">
<span class="marginnote">Typical trajectories for two non-cooperating (green) entities and for the corresponding cooperating unit (blue) on a logarithmic vertical scal (Peters & Adamou, 2018).</span>![](img/emergence-of-cooperation_11_0.png)

As the authors point out:

> In a very literal mathematical sense the whole, $y_1(t)+y_2(t)$, is more than the sum of its parts, $x_1(t) + x_2(t)$. The algebra of cooperation is not merely that of summation.

Next we'll visualize how the total biomass grows for systems of cooperating vs non-cooperating entities with populations $N \in \{2, 3, 4, 5\}$.  

For this, we'll build generators that produce an array of biomasses for each time step.

<p>
<label for="imgbiomass-growth" class="margin-toggle">⊕</label>
<input type="checkbox" id="imgbiomass-growth" class="margin-toggle">
<span class="marginnote">Simulation of the total biomass growth for cooperating vs non-cooperating entities with different populations.</span>
</p>
<div>
<video width="50%" class="bordered" controls>
       <source src="img/biomass-growth.mp4" type="video/mp4">
        Your browser does not support the video tag. </video></div>
