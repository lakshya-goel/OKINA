DROP DATABASE IF EXISTS okina;
CREATE DATABASE okina;
USE okina;

CREATE TABLE administrator(
admin_ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
name VARCHAR(50) NOT NULL,
password VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE adhoc(
adhoc_ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
name VARCHAR(50) NOT NULL,
contact VARCHAR(20) NOT NULL,
position VARCHAR(30) NOT NULL,
INDEX adhoc_name_idx(name)
);

CREATE TABLE assister(
assister_ID INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) NOT NULL,
contact VARCHAR(14) UNIQUE NOT NULL,
INDEX assister_name_idx(name)
);

CREATE TABLE sales(
sales_ID INT AUTO_INCREMENT PRIMARY KEY,
quantity INT NOT NULL,
revenue BIGINT DEFAULT 0,
gross_margin DECIMAL(5, 2) NOT NULL,
date TIMESTAMP NOT NULL,
profit BIGINT DEFAULT 0,
INDEX sales_date_idx(date),
INDEX sales_quantity_idx(quantity)
);

CREATE TABLE merchant(
merchant_ID INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) NOT NULL,
contact VARCHAR(14) UNIQUE NOT NULL,
INDEX merchant_name_idx(name)
);

CREATE TABLE category(
category_ID INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) UNIQUE NOT NULL,
INDEX category_name_idx(name)
);

CREATE TABLE offers(
offers_ID INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(20) UNIQUE NOT NULL,
discount INT NOT NULL,
validity DATE NOT NULL,
INDEX offers_discount_idx(discount),
INDEX offers_validity_idx(validity)
);

CREATE TABLE delivery_exec(
exec_ID INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) NOT NULL,
contact VARCHAR(14) UNIQUE NOT NULL,
availability VARCHAR(30) NOT NULL,
rating DECIMAL(2,1) NOT NULL,
INDEX delivery_exec_name_idx(name)
);

CREATE TABLE inventory(
inventory_ID INT AUTO_INCREMENT PRIMARY KEY,
restock INT NOT NULL,
sales_ID INT NOT NULL,
FOREIGN KEY(sales_ID) REFERENCES sales(sales_ID) ON DELETE CASCADE,
INDEX inventory_sales_idx(sales_ID)
);

CREATE TABLE user(
user_ID INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(50) NOT NULL,
email_id VARCHAR(50) UNIQUE NOT NULL,
password VARCHAR(30) UNIQUE NOT NULL,
INDEX user_email_idx(email_id)
);

CREATE TABLE user_offers(
user_ID INT NOT NULL,
offers_ID INT NOT NULL,
PRIMARY KEY(user_ID, offers_ID),
FOREIGN KEY(user_ID) REFERENCES user(user_ID) ON DELETE CASCADE,
FOREIGN KEY(offers_ID) REFERENCES offers(offers_ID) ON DELETE CASCADE,
INDEX user_offers_offers_idx(offers_ID)
);

CREATE TABLE product(
product_ID INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) NOT NULL,
colour VARCHAR(20),
size VARCHAR(20),
composition VARCHAR(50),
price INT NOT NULL,
discount INT,
rating DECIMAL(4, 2),
category_ID INT NOT NULL,
stock INT NOT NULL,
FOREIGN KEY(category_ID) REFERENCES category(category_ID) ON DELETE CASCADE,
INDEX product_category_idx(category_ID),
INDEX product_price_idx(price)
);

CREATE TABLE delivery_details(
delivery_ID INT AUTO_INCREMENT PRIMARY KEY,
exec_ID INT NOT NULL,
datetime TIMESTAMP NOT NULL,
FOREIGN KEY(exec_ID) REFERENCES delivery_exec(exec_ID) ON DELETE CASCADE,
INDEX delivery_details_datetime_idx(datetime)
);

CREATE TABLE orders(
    order_ID INT AUTO_INCREMENT PRIMARY KEY,
    user_ID INT NOT NULL,
    delivery_ID INT NOT NULL,
    bill INT NOT NULL DEFAULT 0,
    datetime TIMESTAMP NOT NULL,
    FOREIGN KEY(user_ID) REFERENCES user(user_ID) ON DELETE CASCADE,
    FOREIGN KEY(delivery_ID) REFERENCES delivery_details(delivery_ID) ON DELETE CASCADE,
    INDEX(user_ID),
    INDEX(delivery_ID)
);

CREATE TABLE assistance(
    query_ID INT AUTO_INCREMENT PRIMARY KEY,
    order_ID INT NOT NULL,
    user_ID INT DEFAULT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY(order_ID) REFERENCES orders(order_ID) ON DELETE CASCADE,
    FOREIGN KEY(user_ID) REFERENCES user(user_ID) ON DELETE CASCADE,
    INDEX(order_ID),
    INDEX(user_ID)
);

CREATE TABLE invoice(
    invoice_ID INT AUTO_INCREMENT PRIMARY KEY,
    order_ID INT NOT NULL,
    mode_of_payment VARCHAR(49) NOT NULL,
    FOREIGN KEY(order_ID) REFERENCES orders(order_ID) ON DELETE CASCADE,
    INDEX(order_ID)
);

ALTER TABLE sales ADD (
    product_ID INT,
    FOREIGN KEY(product_ID) REFERENCES product(product_ID) ON DELETE CASCADE,
    INDEX(product_ID)
);

CREATE TABLE merchant_products(
    merchant_ID INT NOT NULL,
    product_ID INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY(merchant_ID, product_ID, quantity),
    FOREIGN KEY(product_ID) REFERENCES product(product_ID) ON DELETE CASCADE,
    FOREIGN KEY(merchant_ID) REFERENCES merchant(merchant_ID) ON DELETE CASCADE,
    INDEX(product_ID),
    INDEX(merchant_ID)
);

CREATE TABLE ordered_products(
    order_ID INT NOT NULL,
    product_ID INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY(order_ID, product_ID, quantity),
    FOREIGN KEY(product_ID) REFERENCES product(product_ID) ON DELETE CASCADE,
    FOREIGN KEY(order_ID) REFERENCES orders(order_ID) ON DELETE CASCADE,
    CONSTRAINT qty_ordr CHECK (quantity > 0),
    INDEX(product_ID),
    INDEX(order_ID)
);

CREATE TABLE cart(
    user_ID INT PRIMARY KEY,
    cost INT NOT NULL DEFAULT 0,
    FOREIGN KEY(user_ID) REFERENCES user(user_ID) ON DELETE CASCADE,
    INDEX(user_ID)
);

CREATE TABLE wishlist(
    user_ID INT PRIMARY KEY,
    FOREIGN KEY(user_ID) REFERENCES user(user_ID) ON DELETE CASCADE,
    INDEX(user_ID)
);

CREATE TABLE cart_product(
    user_ID INT NOT NULL,
    product_ID INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY(user_ID, product_ID, quantity),
    FOREIGN KEY(user_ID) REFERENCES cart(user_ID) ON DELETE CASCADE,
    CONSTRAINT qty_crt CHECK (quantity > 0),
    INDEX(user_ID),
    INDEX(product_ID)
);

CREATE TABLE wishlist_product(
    user_ID INT NOT NULL,
    product_ID INT NOT NULL,
    PRIMARY KEY(user_ID, product_ID),
    FOREIGN KEY(user_ID) REFERENCES cart(user_ID) ON DELETE CASCADE,
    INDEX(user_ID),
    INDEX(product_ID)
);

CREATE TABLE user_contact(
    user_ID INT NOT NULL,
    contact VARCHAR(14),
    PRIMARY KEY(user_ID, contact),
    FOREIGN KEY(user_ID) REFERENCES user(user_ID) ON DELETE CASCADE,
    INDEX(user_ID)
);

CREATE TABLE user_address(
    user_ID INT NOT NULL,
    address VARCHAR(250) NOT NULL,
    PRIMARY KEY(user_ID, address),
    FOREIGN KEY(user_ID) REFERENCES user(user_ID) ON DELETE CASCADE,
    INDEX(user_ID)
);

CREATE TABLE user_order_history (
    user_ID INT NOT NULL,
    order_ID INT NOT NULL,
    PRIMARY KEY(user_ID, order_ID),
    FOREIGN KEY(user_ID) REFERENCES user(user_ID) ON DELETE CASCADE,
    FOREIGN KEY(order_ID) REFERENCES orders(order_ID) ON DELETE CASCADE,
    INDEX(user_ID),
    INDEX(order_ID)
);

CREATE TABLE product_tags (
    product_ID INT NOT NULL,
    tag VARCHAR(50) NOT NULL,
    PRIMARY KEY(product_ID, tag),
    FOREIGN KEY(product_ID) REFERENCES product(product_ID) ON DELETE CASCADE,
    INDEX(product_ID),
    INDEX(tag)
);

CREATE TABLE assister_query (
    assister_ID INT NOT NULL,
    query_ID INT NOT NULL,
    PRIMARY KEY(assister_ID, query_ID),
    FOREIGN KEY(assister_ID) REFERENCES assister(assister_ID) ON DELETE CASCADE,
    FOREIGN KEY(query_ID) REFERENCES assistance(query_ID) ON DELETE CASCADE,
    INDEX(assister_ID),
    INDEX(query_ID)
);

DELIMITER //
CREATE TRIGGER BILL_CALC AFTER INSERT ON ORDERED_PRODUCTS
	FOR EACH ROW BEGIN
		UPDATE orders A
		SET bill = bill + (SELECT new.quantity * p.price - ((p.price * discount)/100) FROM product p WHERE p.product_ID = new.product_ID)
		WHERE A.order_ID = NEW.order_ID;
	END //


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

CREATE TRIGGER USR_ID_CHK BEFORE INSERT ON ASSISTANCE 
	FOR EACH ROW BEGIN declare temp_usr INT;
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
	select price - ((price * discount)/100) INTO prod_price
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

CREATE TRIGGER tr_assistance
AFTER INSERT ON assistance
FOR EACH ROW
BEGIN
    SELECT assister_ID
    INTO @chosen_assister
    FROM (
        SELECT assister_ID, COUNT(*) AS num_queries
        FROM assister_query
        GROUP BY assister_ID
        UNION
        SELECT assister_ID, 0 AS num_queries
        FROM assister
        WHERE assister_ID NOT IN (SELECT assister_ID FROM assister_query)
    ) AS counts
    ORDER BY num_queries ASC, assister_id ASC
    LIMIT 1;

    INSERT INTO assister_query(assister_ID, query_ID)
    VALUES (@chosen_assister, NEW.query_ID);
END//

DELIMITER ;


DELIMITER //
CREATE TRIGGER CART_ACOST BEFORE INSERT ON CART_PRODUCT
FOR EACH ROW BEGIN 
	UPDATE cart
	set cost = cost + ( (
	            SELECT price - ((price * discount)/100)
	            FROM product
	            WHERE
	                product_ID = new.product_ID
	        ) * new.quantity
	    )
	WHERE user_ID = new.user_ID;
	END // # cart cost

CREATE TRIGGER CART_SCOST BEFORE DELETE ON CART_PRODUCT
FOR EACH ROW BEGIN 
    DECLARE prod_price INT;
    DECLARE new_cost INT;
    
    SET prod_price = (
        SELECT price - ((price * discount)/100)
        FROM product
        WHERE product_ID = old.product_ID
    );

    SET new_cost = (SELECT cost FROM cart WHERE user_ID = old.user_ID) - (prod_price * old.quantity);
    
    SET new_cost = IF(new_cost < 0, 0, new_cost);
    
    UPDATE cart SET cost = new_cost WHERE user_ID = old.user_ID;
END //

DELIMITER //
CREATE TRIGGER PRD_TGS AFTER INSERT ON product
	for each row BEGIN
    insert into product_tags value(new.product_ID, new.name);
	insert into product_tags value(new.product_ID, new.colour);
 	insert into product_tags value(new.product_ID, new.size);
 	insert into product_tags value(new.product_ID, new.composition);	
    END //

CREATE VIEW user_products AS
select user_ID, p.product_ID, quantity,p.price*quantity as cost from product as p join cart_product as c on p.product_ID = c.product_ID  
order by cost desc

CREATE VIEW see_products AS
select * from product