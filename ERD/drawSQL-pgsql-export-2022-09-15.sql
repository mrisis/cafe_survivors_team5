CREATE TABLE "users"(
    "id" INTEGER NOT NULL,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "phone_number" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "users" ADD PRIMARY KEY("id");
ALTER TABLE
    "users" ADD CONSTRAINT "users_phone_number_unique" UNIQUE("phone_number");
ALTER TABLE
    "users" ADD CONSTRAINT "users_email_unique" UNIQUE("email");
CREATE TABLE "tables"(
    "id" INTEGER NOT NULL,
    "table_number" INTEGER NOT NULL,
    "cafe_space_position" INTEGER NOT NULL,
    "user_id" INTEGER NULL
);
ALTER TABLE
    "tables" ADD PRIMARY KEY("id");
ALTER TABLE
    "tables" ADD CONSTRAINT "tables_table_number_unique" UNIQUE("table_number");
CREATE TABLE "menu_items"(
    "id" INTEGER NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "category" VARCHAR(255) NOT NULL,
    "discount" DOUBLE PRECISION NULL,
    "serving_time_period" TIME(0) WITHOUT TIME ZONE NULL,
    "estimated_cooking_time" TIME(0) WITHOUT TIME ZONE NULL
);
ALTER TABLE
    "menu_items" ADD PRIMARY KEY("id");
CREATE TABLE "orders"(
    "id" INTEGER NOT NULL,
    "table" INTEGER NOT NULL,
    "menu_items" VARCHAR(255) NOT NULL,
    "number" VARCHAR(255) NOT NULL,
    "status" BOOLEAN NOT NULL,
    "timestamp" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "user_id" INTEGER NULL
);
ALTER TABLE
    "orders" ADD PRIMARY KEY("id");
CREATE TABLE "receipts"(
    "id" INTEGER NOT NULL,
    "orders" INTEGER NULL,
    "total_price" DOUBLE PRECISION NOT NULL,
    "final_price" DOUBLE PRECISION NOT NULL,
    "timestamp" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "receipts" ADD PRIMARY KEY("id");
ALTER TABLE
    "tables" ADD CONSTRAINT "tables_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "orders" ADD CONSTRAINT "orders_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "orders" ADD CONSTRAINT "orders_table_foreign" FOREIGN KEY("table") REFERENCES "tables"("id");
ALTER TABLE
    "orders" ADD CONSTRAINT "orders_menu_items_foreign" FOREIGN KEY("menu_items") REFERENCES "menu_items"("id");
ALTER TABLE
    "receipts" ADD CONSTRAINT "receipts_orders_foreign" FOREIGN KEY("orders") REFERENCES "orders"("id");