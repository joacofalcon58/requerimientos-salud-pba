USE GBA_Rendimientos;
GO

BULK INSERT stg.rendimiento_2005_2023
FROM 'C:\Users\joaco\Documents\Porfolio\Rendimientos de establecimientos de salud\rendimiento_2005_2023.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '0x0a',
    CODEPAGE = '65001',
    TABLOCK
);
GO