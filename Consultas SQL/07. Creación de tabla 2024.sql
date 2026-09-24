USE GBA_Rendimientos;
GO

BULK INSERT stg.rendimiento_2024
FROM 'C:\Users\joaco\Documents\Porfolio\Rendimientos de establecimientos de salud\rendimiento_2024.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    CODEPAGE = '65001',
    TABLOCK
);
GO