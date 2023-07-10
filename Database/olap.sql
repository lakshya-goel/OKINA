select
    a.user_ID,
    sum(b.profit) as total_profit,
    b.product_ID
from
    cart_product as a,
    sales as b
where
    a.product_ID = b.product_ID
group by
    a.user_ID,
    b.product_ID with rollup;

#------------
select
    merchant_ID,
    product_ID,
    sum(quantity)
from
    merchant_products
where
    merchant_ID < 10
group by
    merchant_ID,
    product_ID with rollup;

#-----------
select
    a.merchant_ID,
    b.product_ID,
    sum(price) as total_payment
from
    merchant_products as a,
    (
        select
            product_ID,
            (100 - gross_margin) * revenue as price
        from
            sales
        where
            sales_ID < 10
    ) as b
group by
    merchant_ID,
    b.product_ID with rollup;

#-----------
select
    user_ID,
    product_ID,
    count(user_ID) as total_products
from
    cart_product
where
    user_ID < 10
group by
    user_ID,
    product_ID with rollup;

#----------
select
    product_ID,
    year(date),
    month(date),
    sum(profit) as net_profit
from
    sales
group by
    product_ID,
    year(date),
    month(date) with rollup;

#---------
select
    B.category_ID,
    year(A.date),
    month(A.date),
    sum(A.profit) as net_profit
from
    sales A,
    category B,
    product C
where
    A.product_ID = C.product_ID
    and C.category_ID = B.category_ID
group by
    year(A.date),
    month(A.date),
    category_ID with rollup;