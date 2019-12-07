# -*- coding: utf-8 -*-
from odoo import tools
from odoo import models, fields, api
import datetime

class EstimateConversionReport(models.Model):
    _name = 'bb_estimate.estimate_conversion_report'
    _desc = 'Conversion Report'
    _auto = False
    _rec_name = 'Year'
    _order = 'id desc'

    FinancialYear = fields.Char('Financial Year', readonly=True)
    Year = fields.Char('Year', readonly=True)
    Month = fields.Selection([('01','January'), ('02','February'), ('03','March'), ('04','April'), ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'), ('10','October'), ('11','November'), ('12','December')],string='Month',readonly=True)
    TotalEstimate = fields.Integer('Total Estimate',readonly=True)
    ConvertedOrder = fields.Integer('Converted To Order',readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        return """
            SELECT
                id,
                estimate_date_year::text AS "Year",
                estimate_month_desc AS "Month",
                estimate_count AS "TotalEstimate",
                estimate_converted AS "ConvertedOrder",
                CASE
                WHEN estimate_month_desc::int >= 7 THEN estimate_date_year::text || '/' || (estimate_date_year::int + 1)::text
                ELSE (estimate_date_year::int - 1)::text || '/' || estimate_date_year::text
                END as "FinancialYear"
            FROM
                (
                    SELECT
                        id,
                        estimate_date_year,
                        estimate_date_month,
                        estimate_month_desc,
                        (
                            SELECT 
                                count(id) 
                            FROM 
                                bb_estimate_estimate
                            WHERE 
                                extract(month from create_date) = estimate_date_month
                                AND extract(year from create_date) = estimate_date_year
                        ) AS estimate_count,
                        (
                            SELECT 
                                count(id) 
                            FROM 
                                bb_estimate_estimate
                            WHERE 
                                extract(month from create_date) = estimate_date_month
                                AND extract(year from create_date) = estimate_date_year
                                AND "salesOrder" is not NULL
                        ) AS estimate_converted
                    FROM
                        (
                            SELECT
                                min(id) AS id,
                                extract(year from create_date) AS estimate_date_year,
                                extract(month from create_date) AS estimate_date_month,
                                to_char(create_date, 'MM') AS estimate_month_desc
                            FROM
                                bb_estimate_estimate
                            GROUP BY
                                extract(month from create_date),
                                extract(year from create_date),
                                to_char(create_date, 'MM')
                        ) m
                    ) f
        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

class EstimateRatesByMonth(models.Model):
    _name = 'bb_estimate.estimate_rates_months'
    _desc = 'Conversion By Month'
    _auto = False
    _rec_name = 'Year'
    _order = "Year, Month"

    Year = fields.Char('Year', readonly=True)
    Month = fields.Selection([('01','January'), ('02','February'), ('03','March'), ('04','April'), ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'), ('10','October'), ('11','November'), ('12','December')],string='Month',readonly=True)
    TotalEstimates = fields.Integer('Total Estimate', readonly=True)
    ConvertedOrder = fields.Integer('Converted To Order', readonly=True, group_operator="sum")
    ConvertedOrderPercent = fields.Float('Converted To Order(%)', readonly=True, group_operator="avg")

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        return """
            SELECT
                id,
                estimate_month_desc as "Month",
                estimate_date_year::text AS "Year",
                estimate_count AS "TotalEstimates",
                estimate_converted_count AS "ConvertedOrder",
                (estimate_converted_count / estimate_count::float * 100)::integer AS "ConvertedOrderPercent"
            FROM
                (SELECT
                    id,
                    estimate_date_month,
                    estimate_date_year,
                    estimate_month_desc,
                    (
                        SELECT 
                            count(id) 
                        FROM 
                            bb_estimate_estimate
                        WHERE 
                            extract(month from create_date) = estimate_date_month
                            AND extract(year from create_date) = estimate_date_year
                    ) AS estimate_count,
                    (
                        SELECT 
                            count(id) 
                        FROM 
                            bb_estimate_estimate
                        WHERE 
                            extract(month from create_date) = estimate_date_month
                            AND extract(year from create_date) = estimate_date_year
                            AND "salesOrder" is not NULL
                    ) AS estimate_converted_count
                FROM
                    (SELECT
                        min(id) AS id,
                        extract(month from create_date) AS estimate_date_month,
                        extract(year from create_date) AS estimate_date_year,
                        to_char(create_date, 'MM') AS estimate_month_desc
                    FROM
                        bb_estimate_estimate
                    GROUP BY
                        extract(month from create_date),
                        extract(year from create_date),
                        to_char(create_date, 'MM')
                        ) m) f
        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

class EstimateTimesReport(models.Model):
    _name = 'bb_estimate.estimate_times_report'
    _desc = 'Conversion Time Report'
    _auto = False
    _rec_name = 'Year'
    _order = "Year, Month"

    Year = fields.Char('Year', readonly=True)
    Month = fields.Selection([('01','January'), ('02','February'), ('03','March'), ('04','April'), ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'), ('10','October'), ('11','November'), ('12','December')],string='Month',readonly=True)
    AvgConversionTime = fields.Float('Average Conversion Time', group_operator="avg")

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        return """
            SELECT
                id,
                estimate_date_year::text AS "Year",
                estimate_month_desc AS "Month",
                (
                    SELECT 
                        avg(extract(epoch from (s.create_date - e.create_date)) / 3600.0) 
                    FROM 
                        bb_estimate_estimate e
                    INNER JOIN sale_order s on e."salesOrder" = s.id
                    WHERE 
                        extract(month from e.create_date) = estimate_date_month
                        AND extract(year from e.create_date) = estimate_date_year
                ) AS "AvgConversionTime"
            FROM
                (
                    SELECT
                        min(id) AS id,
                        extract(month from create_date) AS estimate_date_month,
                        extract(year from create_date) AS estimate_date_year,
                        to_char(create_date, 'MM') AS estimate_month_desc
                    FROM
                        bb_estimate_estimate
                    WHERE
                        "salesOrder" IS NOT NULL
                    GROUP BY
                        extract(month from create_date),
                        extract(year from create_date),
                        to_char(create_date, 'MM')) m
        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))
