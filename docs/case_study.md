# E-Commerce Analytics Case Study

[Tableau Public dashboard](https://public.tableau.com/app/profile/rustin.khazravi/viz/OlistE-CommerceAnalytics_17914070197460/OlistE-CommerceRevenueDeliveryandSatisfaction)

## The question

I went in with two questions. Where does this marketplace's revenue actually come from, and what makes customers unhappy enough to not come back? Along the way I wanted to test one specific idea: whether delivery speed is worth fixing first.

## Data and approach

Olist is a Brazilian e-commerce marketplace, and the public dataset covers roughly 99,000 orders placed between September 2016 and October 2018, with customers, products, sellers, payments and reviews. I loaded the raw files into DuckDB, used dbt to turn them into a standard set of tables (customers, orders, products and so on), and built SQL views for the numbers a business team would ask about: monthly revenue, how many orders make it through to delivery, repeat purchases, and review scores broken out by segment.

Then I did two things that go past reporting. The first is a quasi-experiment that compares late and on-time deliveries as if they were a test and control group, and is upfront about where that comparison breaks down. The second is a simulated A/B test, where I ran the power analysis and significance testing you'd need if the company actually tried a logistics change.

## What I found

Revenue is concentrated in one state. Total revenue for the period was about R$13.2M, and São Paulo alone brought in R$5.07M of it. That's almost three times the next state, Rio de Janeiro, at R$1.76M. If you're deciding where to put a warehouse or a carrier partnership, you start there.

Most customers never come back. Only 3.12% of customers placed more than one order. This business runs on one-time buyers right now, which makes the first order matter a lot, since an unhappy customer usually doesn't give it a second try.

The order funnel holds up until delivery. 99.8% of placed orders get approved and 97.0% get delivered, so payment and approval aren't the problem. The losses that exist happen later, in fulfillment.

Late delivery lines up with a 1.7-star drop in reviews. 8.1% of delivered orders showed up after the estimated date, and those orders averaged 2.57 stars compared to 4.30 for on-time ones. My first guess was that bigger or farther orders are both slower and more annoying, which would make the gap partly fake. Controlling for order size, freight cost and state barely changed it, though. Among customers who'd been around long enough to come back, the ones with a late order also had a lower repeat rate, 2.90% against 3.84%.

That still doesn't prove late delivery causes bad reviews. Lateness isn't random. It goes along with order size and where the customer lives, so what I have is a strong association. That's why I built the simulated experiment. If Olist wanted to test a fix for real, the sample size math and the analysis are already written.

## What I'd recommend

1. Treat delivery reliability as a retention problem, starting with the states that are late most often. Rio de Janeiro is late on 13.5% of orders and Bahia on 14.0%, compared to 5.9% for São Paulo. Nothing else I looked at was as consistently tied to bad reviews.
2. Run an actual randomized test before spending money on a fix, for example trying a different carrier on a random subset of the routes that run late most. The data I have supports a correlation. A real experiment is what would show cause and effect.
3. Put effort into the first-order experience before something like a loyalty program. With a 3.12% repeat rate, the first order is the only order for most customers, so that's where improvements pay off.

## Limitations

The delivery finding is correlational. Late orders differ from on-time orders in other ways too: they tend to be larger, cost more to ship and cluster in certain states. Controlling for those barely moves the estimate, but things I couldn't measure, like seller reliability, product quality or what each customer expected, could still explain part of the gap. I also left the last six months out of the repeat-purchase analysis, because customers who ordered recently haven't had time to order again and would drag the rate down unfairly. Both decisions are explained in `notebooks/quasi_experiment.ipynb`.
