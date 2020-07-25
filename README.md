# Markov's little supermarket

Simulation is a technique to approximate the behavior of a given system over time.  It allows you to see how a system behaves given certain inputs, and infer best conditions for the goal you want to achieve. 



In this project, I simulated daily life in a supermarket and the transition of customers between different  aisles to answer questions like:

* How long do customer stay in certain areas

* Are there aisles with too many people

* Daily  distribution of customer visits

* How much cashiers do we need to prevent the queues to be too long?

* etc.

  

To do so, I used Markov Chains, a stochastic model used for simulate a sequence of events, based on the current state of the system. In this example, the customer's transition between the individual aisles are the transition between states.  



# Input data and preprocessing

As input, I used a dataset containing data of customers visits and their location in a supermarket. The dataset consisted of 5 .csv files for a fictional week:



|      timestamp      | customer | location |
| :-----------------: | :------: | :------: |
| 2019-09-02 07:03:00 |    1     |  fruits  |
| 2019-09-02 07:05:00 |    1     |  dairy   |
| 2019-09-02 07:05:00 |    2     |  fruits  |

The following data preprocessing were done:

* merge the daily .csv files to one .csv file
* sort by time stamp and customer
* fill up missing timestamps per customer with a forward fill of the current location
* subindex the steps each customers took
* calculate the probability of the start-location by the first occurrence of each customer
  * used for initialization of new customers
* calculate the transition matrix, the probability of customer's next location given his current location 
  * used for determining the next location of a given customer

* calculate the average number of new customer per 15 minutes each day
  * used for determining the number of new customers per time step during the simulation



# How to run it yourself

You can clone the github repository, and run it via the command line. Navigate to the right folder, and enter:

```
python shopping_simulator.py
```

Once you see the screen, press the 'w' letter to start. 



# Requirements

If you quickly want to download all necessary packages, it is the most straight forward to create a new environment. If you have conda, you can enter:

```
conda create --name shopping_simulator --file requirements.txt
```

Then you can run the program, after activating the env:

```
conda activate shopping_simulator
python shopping_simulator.py
```



