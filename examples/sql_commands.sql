-- Цена + объём по монетам
SELECT 
    m.trade_hour,
    ds.symbol,
    m.close,
    m.volume_usd
FROM mart_hourly m
JOIN dim_symbol ds ON ds.id = m.symbol_id
WHERE m.trade_hour >= now() - interval '7 days'
ORDER BY m.trade_hour;

-- Топ 10 монет по hourly_return за прошедшие сутки
WITH first_last AS (
	SELECT
		ds.symbol,
		((LAST_VALUE(mh.close) over w) - (FIRST_VALUE(mh.close) over w)) / FIRST_VALUE(mh.close) OVER w * 100 as daily_return
	FROM mart_hourly mh
	JOIN dim_symbol ds on ds.id=mh.symbol_id
	WHERE mh.trade_hour >= now() - interval '24h'
	WINDOW w as (
		PARTITION BY mh.symbol_id 
		ORDER BY mh.trade_hour
		ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
		)
) 
SELECT
	f.symbol,
	max(f.daily_return) as daily
FROM first_last f
GROUP BY f.symbol
ORDER BY daily DESC
LIMIT 10

-- Волатильность за последние сутки
SELECT 
    ds.symbol,
    m.close,
    m.volatility_24h
FROM mart_hourly m
JOIN dim_symbol ds ON ds.id = m.symbol_id
WHERE m.trade_hour = (SELECT MAX(trade_hour) FROM mart_hourly)
ORDER BY m.volatility_24h DESC NULLS LAST