"""SQL query templates for product-related operations."""

# Categories table queries
CREATE_CATEGORIES_TABLE = """
CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id INTEGER REFERENCES categories(category_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Products table queries
CREATE_PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES categories(category_id),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_physical BOOLEAN DEFAULT TRUE, -- FALSE for services
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Product variants table queries
CREATE_PRODUCT_VARIANTS_TABLE = """
CREATE TABLE IF NOT EXISTS product_variants (
    variant_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    name VARCHAR(100) NOT NULL, -- e.g., "Honey 300g", "Pizza Medium Pepperoni", "Consulting (hourly)"
    sku VARCHAR(50) UNIQUE,
    price DECIMAL(10, 2) NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Inventory table queries
CREATE_INVENTORY_TABLE = """
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id SERIAL PRIMARY KEY,
    variant_id INTEGER NOT NULL REFERENCES product_variants(variant_id),
    quantity INTEGER NOT NULL DEFAULT 0, -- For physical products: actual quantity, for services: available hours
    expiration_date DATE, -- NULL for services or non-perishable products
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Index creation queries
CREATE_PRODUCT_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_categories_parent ON categories(parent_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_variants_product ON product_variants(product_id);
CREATE INDEX IF NOT EXISTS idx_inventory_variant ON inventory(variant_id);
CREATE INDEX IF NOT EXISTS idx_inventory_expiration ON inventory(expiration_date);
"""

# Category queries
GET_CATEGORY_BY_ID = """
SELECT * FROM categories WHERE category_id = %(category_id)s;
"""

GET_CATEGORIES_BY_PARENT = """
SELECT * FROM categories WHERE parent_id = %(parent_id)s;
"""

GET_ROOT_CATEGORIES = """
SELECT * FROM categories WHERE parent_id IS NULL;
"""

CREATE_CATEGORY = """
INSERT INTO categories (name, parent_id)
VALUES (%(name)s, %(parent_id)s)
RETURNING *;
"""

UPDATE_CATEGORY = """
UPDATE categories
SET 
    name = %(name)s,
    parent_id = %(parent_id)s
WHERE category_id = %(category_id)s
RETURNING *;
"""

DELETE_CATEGORY = """
DELETE FROM categories WHERE category_id = %(category_id)s;
"""

# Product queries
GET_PRODUCT_BY_ID = """
SELECT * FROM products WHERE product_id = %(product_id)s;
"""

GET_PRODUCTS_BY_CATEGORY = """
SELECT * FROM products WHERE category_id = %(category_id)s;
"""

GET_PRODUCTS_BY_TYPE = """
SELECT * FROM products WHERE is_physical = %(is_physical)s;
"""

CREATE_PRODUCT = """
INSERT INTO products (category_id, name, description, is_physical)
VALUES (%(category_id)s, %(name)s, %(description)s, %(is_physical)s)
RETURNING *;
"""

UPDATE_PRODUCT = """
UPDATE products
SET 
    category_id = %(category_id)s,
    name = %(name)s,
    description = %(description)s,
    is_physical = %(is_physical)s
WHERE product_id = %(product_id)s
RETURNING *;
"""

DELETE_PRODUCT = """
DELETE FROM products WHERE product_id = %(product_id)s;
"""

# Product variant queries
GET_VARIANT_BY_ID = """
SELECT * FROM product_variants WHERE variant_id = %(variant_id)s;
"""

GET_VARIANTS_BY_PRODUCT = """
SELECT * FROM product_variants WHERE product_id = %(product_id)s;
"""

GET_VARIANT_BY_SKU = """
SELECT * FROM product_variants WHERE sku = %(sku)s;
"""

CREATE_VARIANT = """
INSERT INTO product_variants (product_id, name, sku, price, active)
VALUES (%(product_id)s, %(name)s, %(sku)s, %(price)s, %(active)s)
RETURNING *;
"""

UPDATE_VARIANT = """
UPDATE product_variants
SET 
    name = %(name)s,
    sku = %(sku)s,
    price = %(price)s,
    active = %(active)s
WHERE variant_id = %(variant_id)s
RETURNING *;
"""

DELETE_VARIANT = """
DELETE FROM product_variants WHERE variant_id = %(variant_id)s;
"""

# Inventory queries
GET_INVENTORY_BY_ID = """
SELECT * FROM inventory WHERE inventory_id = %(inventory_id)s;
"""

GET_INVENTORY_BY_VARIANT = """
SELECT * FROM inventory WHERE variant_id = %(variant_id)s;
"""

GET_INVENTORY_BY_EXPIRATION = """
SELECT * FROM inventory WHERE expiration_date <= %(expiration_date)s;
"""

CREATE_INVENTORY = """
INSERT INTO inventory (variant_id, quantity, expiration_date)
VALUES (%(variant_id)s, %(quantity)s, %(expiration_date)s)
RETURNING *;
"""

UPDATE_INVENTORY = """
UPDATE inventory
SET 
    quantity = %(quantity)s,
    expiration_date = %(expiration_date)s,
    last_updated = CURRENT_TIMESTAMP
WHERE inventory_id = %(inventory_id)s
RETURNING *;
"""

UPDATE_INVENTORY_QUANTITY = """
UPDATE inventory
SET 
    quantity = quantity + %(quantity_change)s,
    last_updated = CURRENT_TIMESTAMP
WHERE variant_id = %(variant_id)s
RETURNING *;
"""

DELETE_INVENTORY = """
DELETE FROM inventory WHERE inventory_id = %(inventory_id)s;
"""

# Complex queries for business operations
GET_PRODUCT_WITH_VARIANTS = """
SELECT 
    p.product_id, 
    p.name AS product_name, 
    p.description, 
    p.is_physical,
    c.category_id, 
    c.name AS category_name,
    v.variant_id, 
    v.name AS variant_name, 
    v.sku, 
    v.price, 
    v.active,
    i.quantity, 
    i.expiration_date
FROM 
    products p
JOIN 
    categories c ON p.category_id = c.category_id
LEFT JOIN 
    product_variants v ON p.product_id = v.product_id
LEFT JOIN 
    inventory i ON v.variant_id = i.variant_id
WHERE 
    p.product_id = %(product_id)s;
"""

SEARCH_PRODUCTS = """
SELECT 
    p.product_id, 
    p.name, 
    p.description, 
    p.is_physical,
    c.name AS category_name
FROM 
    products p
JOIN 
    categories c ON p.category_id = c.category_id
WHERE 
    p.name ILIKE %(search_term)s OR 
    p.description ILIKE %(search_term)s OR
    c.name ILIKE %(search_term)s
ORDER BY 
    p.name;
"""

GET_LOW_STOCK_PRODUCTS = """
SELECT 
    p.product_id, 
    p.name AS product_name,
    v.variant_id, 
    v.name AS variant_name, 
    v.sku,
    i.quantity,
    i.expiration_date
FROM 
    products p
JOIN 
    product_variants v ON p.product_id = v.product_id
JOIN 
    inventory i ON v.variant_id = i.variant_id
WHERE 
    i.quantity <= %(threshold)s AND
    p.is_physical = TRUE
ORDER BY 
    i.quantity ASC;
"""