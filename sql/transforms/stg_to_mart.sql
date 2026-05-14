with returns as (
	select
		so.symbol_id,
		so.trade_date as trade_hour,
		so.close,
		so.volume,
		so.quote_volume as volume_usd,
		(so.close - (lag(so.close) over (w)))
		/ lag(so.close) over (w)
		* 100 as hourly_return
	from stg_ohlcv so
	window w as (partition by so.symbol_id order by so.trade_date)
),
calculations as (
	select
		r.symbol_id,
		r.trade_hour,
		r.close,
		r.volume,
		r.volume_usd,
		r.hourly_return,
		stddev(r.hourly_return) over (
			w
			rows between 11 preceding and current row
		) as volatility_12h,
		stddev(r.hourly_return) over (
			w
			rows between 23 preceding and current row
		) as volatility_24h,
		avg(r.close) over (
			w
			rows between 11 preceding and current row
		) as MA12,
		avg(r.close) over (
			w
			rows between 23 preceding and current row
		) as MA24
	from returns r
	window w as (partition by r.symbol_id order by r.trade_hour)
)
insert into mart_hourly (
	symbol_id,	trade_hour, close, volume, volume_usd, hourly_return, volatility_12h, volatility_24h, ma12, ma24
)
select
	c.symbol_id,
	c.trade_hour,
	c.close,
	c.volume,
	c.volume_usd,
	c.hourly_return,
	c.volatility_12h,
	c.volatility_24h,
	c.ma12,
	c.ma24
from calculations c
on conflict (symbol_id, trade_hour) do nothing