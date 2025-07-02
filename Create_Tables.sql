CREATE OR REPLACE TABLE retail.categories (
  category_id INT64 NOT NULL,
  category_name STRING(15) NOT NULL,
  description STRING,
  picture BYTES
);

CREATE OR REPLACE TABLE retail.customer_customer_demo (
  customer_id STRING(5) NOT NULL,
  customer_type_id STRING(5) NOT NULL
);

CREATE OR REPLACE TABLE retail.customer_demographics (
  customer_type_id STRING(5) NOT NULL,
  customer_desc STRING
);

CREATE OR REPLACE TABLE retail.customers (
  customer_id STRING(5) NOT NULL,
  company_name STRING(40) NOT NULL,
  contact_name STRING(30),
  contact_title STRING(30),
  address STRING(60),
  city STRING(15),
  region STRING(15),
  postal_code STRING(10),
  country STRING(15),
  phone STRING(24),
  fax STRING(24)
);

CREATE OR REPLACE TABLE retail.employees (
  employee_id INT64 NOT NULL,
  last_name STRING(20) NOT NULL,
  first_name STRING(10) NOT NULL,
  title STRING(30),
  title_of_courtesy STRING(25),
  birth_date DATE,
  hire_date DATE,
  address STRING(60),
  city STRING(15),
  region STRING(15),
  postal_code STRING(10),
  country STRING(15),
  home_phone STRING(24),
  extension STRING(4),
  photo BYTES,
  notes STRING,
  reports_to INT64,
  photo_path STRING(255)
);

CREATE OR REPLACE TABLE retail.employee_territories (
  employee_id INT64 NOT NULL,
  territory_id STRING(20) NOT NULL
);

CREATE OR REPLACE TABLE retail.order_details (
  order_id INT64 NOT NULL,
  product_id INT64 NOT NULL,
  unit_price FLOAT64 NOT NULL,
  quantity INT64 NOT NULL,
  discount FLOAT64 NOT NULL
);

CREATE OR REPLACE TABLE retail.orders (
  order_id INT64 NOT NULL,
  customer_id STRING(5),
  employee_id INT64,
  order_date DATE,
  required_date DATE,
  shipped_date DATE,
  ship_via INT64,
  freight FLOAT64,
  ship_name STRING(40),
  ship_address STRING(60),
  ship_city STRING(15),
  ship_region STRING(15),
  ship_postal_code STRING(10),
  ship_country STRING(15)
);

CREATE OR REPLACE TABLE retail.products (
  product_id INT64 NOT NULL,
  product_name STRING(40) NOT NULL,
  supplier_id INT64,
  category_id INT64,
  quantity_per_unit STRING(20),
  unit_price FLOAT64,
  units_in_stock INT64,
  units_on_order INT64,
  reorder_level INT64,
  discontinued INT64 NOT NULL
);

CREATE OR REPLACE TABLE retail.region (
  region_id INT64 NOT NULL,
  region_description STRING(60) NOT NULL
);

CREATE OR REPLACE TABLE retail.shippers (
  shipper_id INT64 NOT NULL,
  company_name STRING(40) NOT NULL,
  phone STRING(24)
);

CREATE OR REPLACE TABLE retail.suppliers (
  supplier_id INT64 NOT NULL,
  company_name STRING(40) NOT NULL,
  contact_name STRING(30),
  contact_title STRING(30),
  address STRING(60),
  city STRING(15),
  region STRING(15),
  postal_code STRING(10),
  country STRING(15),
  phone STRING(24),
  fax STRING(24),
  homepage STRING
);

CREATE OR REPLACE TABLE retail.territories (
  territory_id STRING(20) NOT NULL,
  territory_description STRING(60) NOT NULL,
  region_id INT64 NOT NULL
);

CREATE OR REPLACE TABLE retail.us_states (
  state_id INT64 NOT NULL,
  state_name STRING(100),
  state_abbr STRING(2),
  state_region STRING(50)
);



---- Populating the categories table ----

INSERT INTO retail.categories VALUES (1, 'Beverages', 'Soft drinks, coffees, teas, beers, and ales', b' ');
INSERT INTO retail.categories VALUES (2, 'Condiments', 'Sweet and savory sauces, relishes, spreads, and seasonings', b' ');
INSERT INTO retail.categories VALUES (3, 'Confections', 'Desserts, candies, and sweet breads', b' ');
INSERT INTO retail.categories VALUES (4, 'Dairy Products', 'Cheeses', b' ');
INSERT INTO retail.categories VALUES (5, 'Grains/Cereals', 'Breads, crackers, pasta, and cereal', b' ');
INSERT INTO retail.categories VALUES (6, 'Meat/Poultry', 'Prepared meats', b' ');
INSERT INTO retail.categories VALUES (7, 'Produce', 'Dried fruit and bean curd', b' ');
INSERT INTO retail.categories VALUES (8, 'Seafood', 'Seaweed and fish', b'');
