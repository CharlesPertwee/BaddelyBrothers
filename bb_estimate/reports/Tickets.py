from odoo import tools
from odoo import models, fields, api
import datetime

class TicketsTimesReport(models.Model):
    _name = 'bb_estimate.ticket_times_report'
    _desc = 'Conversion Times Report'
    _auto = False
    _rec_name = 'Year'
    _order = "Year, Month"

    FinancialYear = fields.Char('Financial Year', readonly=True)
    Year = fields.Char('Year', readonly=True)
    Month = fields.Selection([('01','January'), ('02','February'), ('03','March'), ('04','April'), ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'), ('10','October'), ('11','November'), ('12','December')],string='Month',readonly=True)
    AvgConversionTime = fields.Float('Average Conversion Time', group_operator="avg", readonly=True)
    OrderType = fields.Selection([('Bespoke','Bespoke'),('Trade Counter','Trade Counter')],'Order Type', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        return """
            SELECT
                id,
                order_date_year::text AS "Year",
                order_month_desc AS "Month",
                order_type AS "OrderType",
                (
                    SELECT 
                        avg(extract(epoch from (create_date - effective_date )) / 3600.0) 
                    FROM 
                        sale_order
                    WHERE 
                        extract(month from create_date) = order_date_month
                        AND extract(year from create_date) = order_date_year
                        AND (CASE WHEN "Estimate" IS NOT NULL THEN 'Bespoke'
                        ELSE 'Trade Counter' END) = m.order_type
                ) AS "AvgConversionTime",
                CASE
                    WHEN order_month_desc::int >= 7 THEN order_date_year::text || '/' || (order_date_year::int + 1)::text
                    ELSE (order_date_year::int - 1)::text || '/' || order_date_year::text
                    END as "FinancialYear"
            FROM
                (
                    SELECT
                        min(id) AS id,
                        extract(month from create_date) AS order_date_month,
                        extract(year from create_date) AS order_date_year,
                        to_char(create_date, 'MM') AS order_month_desc,
                        CASE WHEN "Estimate" IS NOT NULL THEN 'Bespoke'
                        ELSE 'Trade Counter'
                        END AS order_type
                    FROM
                        sale_order
                    WHERE
                        effective_date IS NOT NULL
                    GROUP BY
                        extract(month from create_date),
                        extract(year from create_date),
                        to_char(create_date, 'MM'),
                        CASE WHEN "Estimate" IS NOT NULL THEN 'Bespoke'
                        ELSE 'Trade Counter' END
                        ) m
        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))


class OnTimeDelivery(models.Model):
    _name = 'bb_estimate.on_time_delivery'
    _desc = 'On Time Delivery'
    _auto = False
    _rec_name = 'Year'
    _order = "Year, Month"

    FinancialYear = fields.Char('Financial Year', readonly=True)
    Year = fields.Char('Year', readonly=True)
    Month = fields.Selection([('01','January'), ('02','February'), ('03','March'), ('04','April'), ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'), ('10','October'), ('11','November'), ('12','December')],string='Month',readonly=True)
    JobNumber = fields.Char('Job Number')
    Customer = fields.Char('Customer')
    JobTitle = fields.Char('Job Title')
    OrderDate = fields.Char('OrderDate')
    TargetDispatchDate = fields.Char('Target Dispatch Date')
    ActualDeliveryDate = fields.Char('Actual Delivery Date')
    DeliverySummary = fields.Char('Delivery Summary')

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        return """
            SELECT 
                o.id,
                CASE
                    WHEN extract(month from date_order)::int >= 7 THEN extract(year from date_order)::text || '/' || (extract(year from date_order)::int + 1)::text
                    ELSE (extract(year from date_order)::int - 1)::text || '/' || extract(year from date_order)::text
                END as "FinancialYear",
                extract(year from date_order)::text "Year",
                to_char(date_order,'MM') "Month",
                m.name "JobNumber",
                p.name "Customer",
                e.title "JobTitle",
                to_char(date_order,'dd/MM/yyyy') "OrderDate",
                to_char(o.commitment_date,'dd/MM/yyyy') "TargetDispatchDate",
                to_char(effective_date,'dd/mm/yyyy') "ActualDeliveryDate",
                case 
                    when commitment_date > effective_date then 'Early by '||date_part('day',(commitment_date::timestamp - effective_date::timestamp))||' day(s)'
                    when commitment_date < effective_date then 'Late by '||date_part('day',(effective_Date::timestamp - commitment_date))||' day(s)' 
                    else 'On Time'
                end as "DeliverySummary"
            from sale_order o
            inner join res_partner p on p.id = o.partner_id
            left join bb_estimate_estimate e on e.id = o."Estimate"
            left join mrp_production m on m.id = o."JobTicket" 
            where 
                o.commitment_date is not null
                and o.effective_date is not null
        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

class DeliveryPerfomance(models.Model):
    _name = 'bb_estimate.delivery_performance'
    _desc = 'Delivery Performance'
    _auto = False
    _rec_name = 'Year'
    _order = "Year, Month"

    FinancialYear = fields.Char('Financial Year', readonly=True)
    Year = fields.Char('Year', readonly=True)
    Month = fields.Selection([('01','January'), ('02','February'), ('03','March'), ('04','April'), ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'), ('10','October'), ('11','November'), ('12','December')],string='Month',readonly=True)
    Early = fields.Integer('Early Orders')
    OnTime = fields.Integer('On-Time Orders')
    Delayed = fields.Integer('Delayed Orders')
    DeliverySummary = fields.Char('Delivery Summary')

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        return """
            select 
                id,
                "FinancialYear",
                "Year",
                "Month",
                (
                        select count AS "Early" from (
                            SELECT 
                                count(id) as count,
                                sum(date_part('day',(commitment_date::timestamp - effective_date::timestamp))) as early
                            from sale_order 
                            where to_char(date_order,'MM') = o."Month" and to_char(date_order,'YYYY')= o."Year"
                            group by to_char(date_order,'YYYY'),to_char(date_order,'MM')
                        ) P where p.early > 0
                    ),
                    (
                        select count AS "OnTime" from (
                            SELECT 
                                count(id) as count,
                                sum(date_part('day',(commitment_date::timestamp - effective_date::timestamp))) as on_time
                            from sale_order 
                            where to_char(date_order,'MM') = o."Month" and to_char(date_order,'YYYY')= o."Year"
                            group by to_char(date_order,'YYYY'),to_char(date_order,'MM')
                        ) P where p.on_time = 0
                    ),
                    (
                        select count AS "Delayed" from (
                            SELECT 
                                count(id) as count,
                                sum(date_part('day',(commitment_date::timestamp - effective_date::timestamp))) as late
                            from sale_order 
                            where to_char(date_order,'MM') = o."Month" and to_char(date_order,'YYYY')= o."Year"
                            group by to_char(date_order,'YYYY'),to_char(date_order,'MM')
                        ) P where p.late < 0
                    ),
                    (case when delivery_summary > 0 then 'Early by '|| delivery_summary ||' day(s)'  
                        when delivery_summary < 0 then 'Late by '|| delivery_summary ||' day(s)'
                        else 'On Time'  
                    end
                    ) as "DeliverySummary"
                from
                (SELECT
                    min(id) AS id,
                    CASE
                        WHEN extract(month from date_order)::int >= 7 THEN extract(year from date_order)::text || '/' || (extract(year from date_order)::int + 1)::text
                        ELSE (extract(year from date_order)::int - 1)::text || '/' || extract(year from date_order)::text
                    END as "FinancialYear",
                    extract(year from date_order)::text "Year",
                    to_char(date_order,'MM') "Month",
                    round(avg(date_part('day',(commitment_date::timestamp - effective_date::timestamp)))::numeric,2) as delivery_summary
                FROM
                    sale_order 
                GROUP BY
                    extract(month from date_order),
                    extract(year from date_order),
                    to_char(date_order, 'MM')
                ) o

        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))