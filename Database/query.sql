DELIMITER //
CREATE TRIGGER USER_CART AFTER INSERT ON USER
	for each row BEGIN
    insert into cart(user_ID) value(new.user_ID);
    END //#cart create check

DELIMITER //
CREATE TRIGGER WISH_UN_LIST AFTER INSERT ON PRODUCT
	for each row BEGIN
    delete from wishlist_product where product_ID = new.product_ID;
	
    END //#wish list check

DELIMITER //
CREATE TRIGGER FILL_INVENTORY BEFORE UPDATE ON PRODUCT
	FOR EACH ROW IF new.stock = 0
    THEN
    BEGIN
    set new.stock=(select A.restock from inventory A, sales B 
    where A.sales_ID = B.sales_ID and B.product_ID = old.product_ID);
    update inventory A set restock = (select quantity from sales where sales_ID = A.sales_ID);
	END;
    end if;
	//#restocking product from inventory


DELIMITER //

CREATE TRIGGER USR_ID_CHK BEFORE INSERT ON ASSISTANCE 
	FOR EACH ROW BEGIN atomic declare temp_usr INT;
	if new.order_ID != 0 then
	select user_ID INTO temp_usr
	from orders
	where order_ID = new.order_ID;
	else set temp_usr := floor(rand()*(5000))+1;
	end if;
	set new.user_ID = temp_usr;
	END//# assistance trigger 


DELIMITER //

CREATE TRIGGER SALES_REC BEFORE INSERT ON ORDERED_PRODUCTS 
FOR EACH ROW BEGIN 
	declare prod_price INT;
	select price INTO prod_price
	FROM product
	WHERE
	    product.product_ID = new.product_ID;
	update sales
	set
	    quantity = quantity + new.quantity
	WHERE
	    sales.product_ID = new.product_ID;
	update sales
	set
	    revenue = sales.quantity * prod_price
	WHERE
	    sales.product_ID = new.product_ID;
	update sales
	set
	    profit = (gross_margin * sales.revenue) / 100
	WHERE
	    sales.product_ID = new.product_ID;
	END// # sales revenue 


DELIMITER //


CREATE TRIGGER CART_COST BEFORE INSERT ON CART_PRODUCT 
FOR EACH ROW BEGIN 
	UPDATE cart
	set cost = cost + ( (
	            SELECT price
	            FROM product
	            WHERE
	                product_ID = new.product_ID
	        ) * new.quantity
	    )
	WHERE user_ID = new.user_ID;
	END // # cart cost

#join cart and product
SELECT
    A.product_ID,
    B.name,
    A.quantity
FROM cart_product A
    JOIN product B ON (A.user_ID = 1 AND A.product_ID = B.product_ID);

#join cart and product
SELECT
    A.product_ID,
    A.quantity
FROM cart_product A FULL OUTER
    JOIN product B ON A.product_ID = B.product_ID WHERE A.user_ID = 1 ;

#union wishlist and cart
SELECT A.product_ID, B.name
FROM cart_product A, product B
WHERE
	A.user_ID = 1
	AND A.product_ID = B.product_ID
UNION
SELECT A.product_ID, B.name
FROM
	wishlist_product A,
	product B
WHERE
	A.user_ID = 1
	AND A.product_ID = B.product_ID;

#cartesian of offers and cart
select
	cart.user_ID,
	cart.cost,
	offers.name,
	offers.discount,
	offers.validity, (
		cart.cost * (100 - offers.discount)
	) / 100
from cart
	CROSS JOIN offers;
	
#delivery details
select
	A.order_ID,
	B.datetime,
	C.name,
	C.phone
FROM
	orders A,
	delivery_details B,
	delivery_exec C
WHERE
	A.delivery_ID = B.delivery_ID
	AND B.exec_ID = C.exec_ID; 

# select products based on size and rating ordered by price
select *
from product
where
	size = 'XL'
	AND rating >= 4.00
ORDER BY price; 

# best seller 
select *
from product
where (
		SELECT quantity
		FROM sales
		where
			sales.product_ID = product.product_ID
	) > 950000;

#min and max price in a category
select
    category.name,
    min(price),
    max(price),
	avg(price)
FROM product
    JOIN category ON product.category_ID = category.category_ID
GROUP BY name;

#average order quantity of a product
select
    product.name,
    AVG(quantity)
FROM ordered_products
    JOIN product ON ordered_products.product_ID = product.product_ID
GROUP BY name;

#delete user
delete from user
where user_ID = 1 AND NOT EXISTS(
        select *
        from orders
        WHERE user_ID = 1
    );

#discount constraint
ALTER TABLE
    offers add constraint check (discount > 0);

#count
SELECT distinct name, count(*)
from product
WHERE size = 'XL' OR 'L' OR '3XL'
group by name HAVING count(*)>1;

#users who ordered a product
SELECT user_ID, username
FROM user
WHERE user.user_ID IN (
        SELECT user_ID
        from orders
        WHERE orders.order_ID IN (
                SELECT order_ID
                FROM ordered_products
                WHERE
                    product_ID = 3063
            )

);

#check table data
desc cart_product;
select * from cart_product where quantity<=0;
desc offers;
select * from offers where discount<=0;
desc ordered_products;
select * from ordered_products where quantity<=0;
desc category
select * from category where name = '#74463c';
desc user;
desc administrator;
desc merchant;
desc delivery_exec;



