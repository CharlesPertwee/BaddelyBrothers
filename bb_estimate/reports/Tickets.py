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
                        avg(extract(epoch from (create_date - effective_date)) / 3600.0) 
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
