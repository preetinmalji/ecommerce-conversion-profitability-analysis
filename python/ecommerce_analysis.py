# E-Commerce Profitability & Customer Analysis
# Author: [Preeti Malji]
# Description:
# This script performs order-level and customer-level analysis
# to evaluate profitability, customer value, and channel efficiency.

# 1. IMPORT LIBRARIES
import os
import pandas as pd
import numpy as np

print("Files in directory:")
print(os.listdir())


# 2. LOAD DATA

funnel = pd.read_csv('funnel_data.csv')
orders = pd.read_csv('orders_data.csv')

print("\nFunnel Data Preview:")
print(funnel.head())

print("\nOrders Data Preview:")
print(orders.head())

print("\nFunnel Columns:", funnel.columns)
print("Orders Columns:", orders.columns)



# 3. SIMULATE PAYMENT FAILURE

# Note: Payment status is simulated to analyze revenue leakage

orders['payment_status'] = np.where(
    np.random.rand(len(orders)) < 0.7,
    'failed',
    'success'
)

print("\nPayment Status Distribution:")
print(orders['payment_status'].value_counts())



# 4. APPLY DISCOUNT LOGIC

# Simulating discount impact on final price

orders['discount'] = orders['order_value'] * np.random.uniform(0.1, 0.3)
orders['final_price'] = orders['order_value'] - orders['discount']

print("\nSample Discount Calculation:")
print(orders[['order_value', 'discount', 'final_price']].head())



# 5. ADD CUSTOMER ACQUISITION COST (CAC)

# Approximate CAC based on channel

channel_cac = {
    'google': 300,
    '(direct)': 50,
    'referral': 150
}

orders['cac'] = orders['channel'].map(channel_cac).fillna(200)

print("\nSample CAC Mapping:")
print(orders[['channel', 'cac']].head())


# 6. CALCULATE PROFIT PER ORDER
orders['profit'] = orders['final_price'] - orders['cac']

print("\nProfit Calculation Sample:")
print(orders[['order_value', 'final_price', 'cac', 'profit']].head())


# 7. REVENUE LEAKAGE ANALYSIS
# Revenue lost due to failed payments

failed_orders = orders[orders['payment_status'] == 'failed']
lost_revenue = failed_orders['order_value'].sum()

print("\nTotal Revenue Lost due to Payment Failure:", lost_revenue)


# 8. LOSS-MAKING ORDERS ANALYSIS
loss_orders = orders[orders['profit'] < 0]

print("\nNumber of Loss-Making Orders:", len(loss_orders))


# 9. CHANNEL-LEVEL PROFITABILITY
channel_profit = orders.groupby('channel')['profit'].mean().sort_values()

print("\nChannel-Level Profitability (Avg Profit per Order):")
print(channel_profit)


# 10. CUSTOMER-LEVEL AGGREGATION
customer_orders = orders.groupby('user_id').agg({
    'order_value': 'sum',
    'order_id': 'count'
}).reset_index()

customer_orders.columns = ['user_id', 'total_spent', 'num_orders']

print("\nCustomer Aggregation Sample:")
print(customer_orders.head())


# 11. CUSTOMER SEGMENTATION

# Segment into repeat vs one-time customers

customer_orders['customer_type'] = customer_orders['num_orders'].apply(
    lambda x: 'repeat' if x > 1 else 'one-time'
)

print("\nCustomer Type Distribution:")
print(customer_orders['customer_type'].value_counts())

print("\nAverage Spend by Customer Type:")
print(customer_orders.groupby('customer_type')['total_spent'].mean())



# 12. LIFETIME VALUE (LTV)

# LTV = total customer spend

customer_orders['avg_order_value'] = (
    customer_orders['total_spent'] / customer_orders['num_orders']
)

customer_orders['ltv'] = (
    customer_orders['avg_order_value'] * customer_orders['num_orders']
)

print("\nCustomer LTV Sample:")
print(customer_orders.head())



# 13. LTV vs CAC ANALYSIS

customer_cac = orders.groupby('user_id')['cac'].mean().reset_index()

customer_orders = customer_orders.merge(customer_cac, on='user_id', how='left')

customer_orders['net_value'] = customer_orders['ltv'] - customer_orders['cac']

print("\nCustomer Net Value Sample:")
print(customer_orders.head())

print("\nNet Value Distribution:")
print(customer_orders['net_value'].describe())


# 14. UNPROFITABLE CUSTOMERS

loss_customers = customer_orders[customer_orders['net_value'] < 0]

print("\nNumber of Unprofitable Customers:", len(loss_customers))



# 15. EXPORT FINAL DATASETS

orders.to_csv("final_orders.csv", index=False)
customer_orders.to_csv("customer_ltv.csv", index=False)

print("\nFiles exported successfully.")



# 16. FINAL DATA PREVIEW

print("\nFinal Funnel Data Preview:")
print(funnel.head())

print("\nFinal Orders Data Preview:")
print(orders.head())
