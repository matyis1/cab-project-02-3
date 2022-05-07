INSERT INTO Building (portfolio_manager_id, property_name, property_type, year_built, gross_floor_area, factor) VALUES ('0', 'testing', 'STEM', 1998, 128, 1);

INSERT INTO Building (portfolio_manager_id, property_name, property_type, year_built, gross_floor_area) VALUES ('0', 'testing', 'STEM', 1998, 128);

INSERT INTO Meter (meter_name, portfolio_manager_meter_id, meter_type, units, portfolio_manager_id) VALUES ('m0', '1638', 'Gas', 'KwHr', '0'); 

INSERT INTO Meter_Entry (meter_consumption_id, usage_quantity_total, cost_total, start_date, end_date, meter_name) VALUES ('testid', 420, 1240, '2020-10-05 14:01:10-08', '2020-10-05 14:11:10-08', 'm0');

