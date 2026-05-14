insert into stg_ohlcv (
	symbol_id,	trade_date, open, high, low, close, volume, quote_volume,	trades_count
)
select distinct on (ds.id, to_timestamp(ro.open_time/1000)::timestamptz)
	ds.id as symbol_id,
	to_timestamp(ro.open_time/1000)::timestamptz as trade_date,
	ro.open,
	ro.high,
	ro.low,
	ro.close,
	ro.volume,
	ro.quote_asset_volume as quote_volume,
	ro.number_of_trades
from raw_ohlcv ro
join dim_symbol ds on ds.symbol = ro.symbol
where 
	ro.open 				> 0 and 
	ro.low 					> 0 and
	ro.close				> 0 and 
	ro.open_time 			> 0 and
	ro.volume				>= 0 and
	ro.quote_asset_volume	>= 0 and
	ro.number_of_trades		>= 0 and
	ro.symbol				is not null and
	ro.high					>= ro.low
order by ds.id, to_timestamp(ro.open_time/1000)::timestamptz, ro.loaded_at desc
on conflict (symbol_id, trade_date) do nothing;