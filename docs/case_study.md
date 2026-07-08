# E-Commerce Analytics Case Study

## Business question

Where does this business's revenue concentrate, and what drives customer
dissatisfaction and churn risk? This analysis uses two years of order-level
data from a Brazilian e-commerce marketplace, Olist, to answer both
questions and to test whether one specific operational lever, delivery
speed, is worth prioritizing.

## Data and method

The dataset covers roughly 99,000 orders placed between September 2016 and
October 2018, including customers, products, sellers, payments, and delivery
reviews. I loaded the raw data into a warehouse, organized it into a
standard set of business tables (customers, orders, products), and rolled
it up into metrics leadership can act on directly: monthly revenue, order
completion rates, repeat purchase behavior, and customer satisfaction by
segment.

Two more analyses go past simple reporting. First, a **quasi-experiment**
treats late and on-time deliveries as a controlled test would, and spells
out exactly where real-world data falls short of a true randomized trial.
Second, a **simulated randomized test** shows the statistical tooling
(required sample sizes, significance testing) is ready for when a real
experiment, like a logistics change, gets the green light.

## Findings

**Revenue concentrates in one state.** Total revenue across the period was
about R$13.2M. São Paulo alone accounts for R$5.07M of that, more than
double the next-largest state, Rio de Janeiro, at R$1.76M. Any investment
in warehousing, carrier partnerships, or marketing should start there.

**Most customers don't come back.** Only 3.12% placed more than one order.
This business runs on single-purchase customers today. First-order
experience carries the weight, since a dissatisfied customer rarely gets a
second chance to change their mind.

**The order funnel holds up until delivery.** Of orders placed, 99.8% get
approved and 97.0% get delivered. Payment and approval aren't where orders
get lost. What drop-off exists happens later, in fulfillment.

**Late delivery predicts a 1.7-star review gap.** 7.7% of delivered orders
arrive after the estimated delivery date. Those orders average a 2.57-star
review. On-time orders average 4.22 stars. Controlling for order size,
freight cost, and state barely narrows the gap: bigger or farther orders
being both slower and less satisfying doesn't explain it. Among customers
with enough time in the dataset to have returned, late orders also show a
lower repeat-purchase rate, 2.90% versus 3.84%.

**The tooling for a real test already exists.** Delivery lateness isn't
randomly assigned. It correlates with order size and customer location, so
the finding above is an association, not proof that fixing delivery speed
fixes satisfaction. A companion simulation walks through the mechanics a
real randomized logistics experiment would need: a power analysis to size
the test, then a significance test to read the result. That groundwork
won't need redoing when the time comes.

## Recommendation

1. **Prioritize delivery reliability as a retention lever**, starting with
   the states with the highest late-delivery rates: Rio de Janeiro at 13.5%
   and Bahia at 14.0%, against São Paulo's 5.9%. Nothing else in this
   analysis drives dissatisfaction as consistently.
2. **Run a real randomized experiment before committing to a fix.** Test an
   alternate carrier or shipping method on a randomly assigned subset of
   high-late-rate routes. The dataset supports a correlational claim. A
   randomized test earns a causal one.
3. **Treat first-order experience as the primary lever for growth**, over
   loyalty programs aimed at repeat customers. With a 3.12% repeat rate, the
   highest-leverage improvements are the ones that touch a customer's first
   order, since for most customers that's also their only order.

## Limitations

The delivery-lateness finding is correlational. Orders that arrive late
differ from on-time orders in other ways too: they tend to be larger, cost
more in freight, and cluster in certain states. Controlling for those
factors barely changes the estimated effect, but unmeasured factors, like
seller reliability, product quality, or individual customer expectations,
could still explain part of the gap. The repeat-purchase analysis excludes
the final six months of the dataset too, so recent orders that haven't had
time to generate a second purchase don't get penalized for it. Both choices
are spelled out in `notebooks/quasi_experiment.ipynb`.
