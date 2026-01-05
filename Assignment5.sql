SELECT 
	s.SymbolName,
	o.Direction,
	o.Volume
FROM [OrderTest] o
INNER JOIN SymbolTest s ON o.SymbolId = s.SymbolId 
WHERE s.SymbolId = 1;

SELECT 
    s.SymbolName,
    ABS(SUM(CASE 
        WHEN o.Direction = 'BUY' THEN o.Volume 
        WHEN o.Direction = 'SELL' THEN -o.Volume 
        ELSE 0 
    END)) AS TotalVolumeCalculated,
    -- Penentuan Direction tetap berdasarkan nilai asli (sebelum di-ABS)
    CASE 
        WHEN SUM(CASE WHEN o.Direction = 'BUY' THEN o.Volume WHEN o.Direction = 'SELL' THEN -o.Volume ELSE 0 END) > 0 THEN 'BUY'
        WHEN SUM(CASE WHEN o.Direction = 'BUY' THEN o.Volume WHEN o.Direction = 'SELL' THEN -o.Volume ELSE 0 END) < 0 THEN 'SELL'
        ELSE 'NEUTRAL'
    END AS FinalDirection
FROM [OrderTest] o
INNER JOIN SymbolTest s ON o.SymbolId = s.SymbolId 
WHERE s.SymbolId = 1
GROUP BY s.SymbolName;