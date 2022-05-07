CREATE TABLE Building (
portfolio_manager_id varchar(9) PRIMARY KEY, 
property_name varchar(255), 
property_type varchar(255), 
year_built INT,
gross_floor_area INT NOT NULL CHECK (gross_floor_area > 0),
factor FLOAT); 

CREATE TABLE Meter (
meter_name varchar(9) PRIMARY KEY,
portfolio_manager_meter_id varchar(255),
meter_type varchar(255),
units varchar(255));

CREATE TABLE Meter_Entry (
meter_consumption_id varchar(255) PRIMARY KEY,
usage_quantity_total varchar(20),
cost_total varchar(20),
start_date DATE,
end_date DATE,
meter_name varchar(9),
FOREIGN KEY (meter_name) REFERENCES Meter (meter_name) MATCH FULL);


