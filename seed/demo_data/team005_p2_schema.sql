-- CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
CREATE USER IF NOT EXISTS gatechUser@localhost IDENTIFIED BY 'gatech123';
DROP DATABASE IF EXISTS `cs6400_fa22_team005`; 
SET default_storage_engine=InnoDB;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS cs6400_fa22_team005 
    DEFAULT CHARACTER SET utf8mb4 
    DEFAULT COLLATE utf8mb4_unicode_ci;
USE cs6400_fa22_team005;
GRANT SELECT, INSERT, UPDATE, DELETE, FILE ON *.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON `gatechuser`.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON `cs6400_fa22_team005`.* TO 'gatechUser'@'localhost';
FLUSH PRIVILEGES;

-- Tables
CREATE TABLE Household (
  email varchar(250) NOT NULL,
  square_footage int(11) NOT NULL,
  number_of_occupants int(11) NOT NULL,
  number_of_bedrooms int(11) NOT NULL,
  type varchar(100) NOT NULL,
  postal_code varchar(100) NOT NULL,
  PRIMARY KEY (email)
);
CREATE TABLE PhoneNumber (
  email varchar(250) NOT NULL,
  area_code varchar(100) NOT NULL,
  last_7_digits varchar(100) NOT NULL,
  type varchar(100) NOT NULL,
  PRIMARY KEY (area_code, last_7_digits)
);
CREATE TABLE Location (
  postal_code varchar(250) NOT NULL,
  city varchar(100) NOT NULL,
  state varchar(100) NOT NULL,
  latitude DECIMAL (10, 6) NOT NULL,
  longitude DECIMAL (10, 6) NOT NULL,
  PRIMARY KEY (postal_code)
);
CREATE TABLE HalfBathroom (
  email varchar(250) NOT NULL,
  bathroom_order int(11) NOT NULL,
  number_of_sinks int(11) NOT NULL,
  number_of_commodes int(11) NOT NULL,
  number_of_bidets int(11) NOT NULL,
  name varchar(100) NULL,
  PRIMARY KEY (email, bathroom_order)
);
CREATE TABLE FullBathroom (
  email varchar(250) NOT NULL,
  bathroom_order int(11) NOT NULL,
  number_of_sinks int(11) NOT NULL,
  number_of_commodes int(11) NOT NULL,
  number_of_bidets int(11) NOT NULL,
  number_of_bathtubs int(11) NOT NULL,
  number_of_showers int(11) NOT NULL,
  number_of_tubs_showers int(11) NOT NULL,
  whether_primary TINYINT NOT NULL,
  PRIMARY KEY (email, bathroom_order)
);
CREATE TABLE Manufacturer (
  manufacturer varchar(100) NOT NULL,
  PRIMARY KEY (manufacturer)
);
CREATE TABLE RefrigeratorFreezer (
  email varchar(250) NOT NULL,
  appliance_order int(11) NOT NULL,
  model_name varchar(100) NULL,
  manufacturer varchar(100) NOT NULL,
  type varchar(100) NOT NULL,
  PRIMARY KEY (email, appliance_order)
);
CREATE TABLE Cooker (
  email varchar(250) NOT NULL,
  appliance_order int(11) NOT NULL,
  model_name varchar(100) NULL,
  manufacturer varchar(100) NOT NULL,
  PRIMARY KEY (email, appliance_order)
);
CREATE TABLE Oven (
  email varchar(250) NOT NULL,
  appliance_order int(11) NOT NULL,
  type varchar(100) NOT NULL,
  PRIMARY KEY (email, appliance_order)
);
CREATE TABLE OvenHeatSource (
  email varchar(250) NOT NULL,
  appliance_order int(11) NOT NULL,
  heat_source varchar(100) NOT NULL,
  PRIMARY KEY (email, appliance_order, heat_source)
);
CREATE TABLE Cooktop (
  email varchar(250) NOT NULL,
  appliance_order int(11) NOT NULL,
  heat_source varchar(100) NOT NULL,
  PRIMARY KEY (email, appliance_order)
);
CREATE TABLE Washer (
  email varchar(250) NOT NULL,
  appliance_order int(11) NOT NULL,
  model_name varchar(100) NULL,
  manufacturer varchar(100) NOT NULL,
  loading_type varchar(100) NOT NULL,
  PRIMARY KEY (email, appliance_order)
);
CREATE TABLE Dryer (
  email varchar(250) NOT NULL,
  appliance_order int(11) NOT NULL,
  model_name varchar(100) NULL,
  manufacturer varchar(100) NOT NULL,
  heat_source varchar(100) NOT NULL,
  PRIMARY KEY (email, appliance_order)
);
CREATE TABLE TV (
  email varchar(250) NOT NULL,
  appliance_order int(11) NOT NULL,
  model_name varchar(100) NULL,
  manufacturer varchar(100) NOT NULL,
  display_type varchar(100) NOT NULL,
  display_size DECIMAL (10, 6) NOT NULL,
  maximum_resolution varchar(100) NOT NULL,
  PRIMARY KEY (email, appliance_order)
);

-- Constraints   Foreign Keys: FK_ChildTable_childColumn_ParentTable_parentColumn
ALTER TABLE Household
  ADD CONSTRAINT fk_Household_postal_code_Location_postal_code
  FOREIGN KEY (postal_code) REFERENCES Location (postal_code);
ALTER TABLE PhoneNumber
  ADD CONSTRAINT fk_PhoneNumber_email_Household_email
  FOREIGN KEY (email) REFERENCES Household (email)
  ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE HalfBathroom
  ADD CONSTRAINT fk_HalfBathroom_email_Household_email
  FOREIGN KEY (email) REFERENCES Household (email)
  ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE FullBathroom
  ADD CONSTRAINT fk_FullBathroom_email_Household_email
  FOREIGN KEY (email) REFERENCES Household (email)
  ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE RefrigeratorFreezer
  ADD CONSTRAINT fk_RefrigeratorFreezer_email_Household_email
  FOREIGN KEY (email) REFERENCES Household (email)
  ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE RefrigeratorFreezer
  ADD CONSTRAINT fk_RefrigeratorFreezer_manufacturer_Manufacturer_manufacturer
  FOREIGN KEY (manufacturer) REFERENCES Manufacturer (manufacturer);
ALTER TABLE Cooker
  ADD CONSTRAINT fk_Cooker_email_Household_email
  FOREIGN KEY (email) REFERENCES Household (email)
  ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Cooker
  ADD CONSTRAINT fk_Cooker_manufacturer_Manufacturer_manufacturer
  FOREIGN KEY (manufacturer) REFERENCES Manufacturer (manufacturer);
ALTER TABLE Oven
  ADD CONSTRAINT fk_Oven_email_appliance_order_Cooker_email_appliance_order
  FOREIGN KEY (email, appliance_order) REFERENCES Cooker (email, appliance_order)
  ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE OvenHeatSource
  ADD CONSTRAINT fk_OvenHeatSource_email_appliance_order_Oven_email_appliance_order
  FOREIGN KEY (email, appliance_order) REFERENCES Oven (email, appliance_order)
  ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Cooktop
  ADD CONSTRAINT fk_Cooktop_email_appliance_order_Cooker_email_appliance_order
  FOREIGN KEY (email, appliance_order) REFERENCES Cooker (email, appliance_order)
  ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Washer
  ADD CONSTRAINT fk_Washer_email_Household_email
  FOREIGN KEY (email) REFERENCES Household (email)
  ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Washer
  ADD CONSTRAINT fk_Washer_manufacturer_Manufacturer_manufacturer
  FOREIGN KEY (manufacturer) REFERENCES Manufacturer (manufacturer);
ALTER TABLE Dryer
  ADD CONSTRAINT fk_Dryer_email_Household_email
  FOREIGN KEY (email) REFERENCES Household (email)
  ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Dryer
  ADD CONSTRAINT fk_Dryer_manufacturer_Manufacturer_manufacturer
  FOREIGN KEY (manufacturer) REFERENCES Manufacturer (manufacturer);
ALTER TABLE TV
  ADD CONSTRAINT fk_TV_email_Household_email
  FOREIGN KEY (email) REFERENCES Household (email)
  ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE TV
  ADD CONSTRAINT fk_TV_manufacturer_Manufacturer_manufacturer
  FOREIGN KEY (manufacturer) REFERENCES Manufacturer (manufacturer);
