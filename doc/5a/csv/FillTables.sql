\COPY Building (portfolio_manager_id, property_name, property_type, year_built, gross_floor_area, factor) FROM 'Properties.csv' DELIMITER ',' CSV HEADER;

\COPY Meter (meter_name, portfolio_manager_meter_id, meter_type, units) FROM 'Meters.csv' DELIMITER ',' CSV HEADER;

\COPY Meter_Entry (meter_consumption_id, usage_quantity_total, cost_total, start_date, end_date, meter_name) FROM 'Meter_Entries.csv' DELIMITER ',' CSV HEADER;

