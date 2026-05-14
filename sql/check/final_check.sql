select 
count(*) as count,
'duplicates' as check_name
from (
	select 
		symbol_id, 
		trade_hour
	from mart_hourly
	group by symbol_id, trade_hour
	having COUNT(*) > 1) dups

union all 
	
select
	count(*),
	'nulls' as check_name
from mart_hourly tmh
where close is null
or volume is null 
or symbol_id is null
or trade_hour is null
or close <= 0