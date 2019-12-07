# -*- coding: utf-8 -*-
from odoo import tools
from odoo import models, fields, api
import datetime

class LeadConversionReport(models.Model):
    _name = 'bb_estimate.lead_conversion_report'
    _desc = 'Conversion Report'
    _auto = False
    _rec_name = 'Year'
    _order = 'id desc'

    FinancialYear = fields.Char('Financial Year', readonly=True)
    Year = fields.Char('Year', readonly=True)
    Month = fields.Selection([('01','January'), ('02','February'), ('03','March'), ('04','April'), ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'), ('10','October'), ('11','November'), ('12','December')],string='Month',readonly=True)
    EnquiryType = fields.Selection([('Envelope Estimate','Envelope Estimate'),('Print Estimate','Print Estimate')], string='Enquiry Type',readonly=True)
    TotalEnquiry = fields.Integer('Total Enquiries',readonly=True)
    ConvertedEnquriy = fields.Integer('Converted To Estimate',readonly=True)
    ConvertedOrder = fields.Integer('Converted To Order',readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        return """

            SELECT
                id,
                CASE
                WHEN enquiry_month_desc::int >= 7 THEN enquiry_date_year::text || '/' || (enquiry_date_year::int + 1)::text
                ELSE (enquiry_date_year::int - 1)::text || '/' || enquiry_date_year::text
                END as "FinancialYear",
                enquiry_date_year::text AS "Year",
                enquiry_month_desc as "Month",
                enquiry_type as "EnquiryType",
                enquiry_count as "TotalEnquiry",
                enquiry_converted_count as "ConvertedEnquriy",
                enquiry_order_count as "ConvertedOrder"
            FROM
                (
                SELECT
                    id,
                    enquiry_date_month,
                    enquiry_date_year,
                    enquiry_month_desc,
                    enquiry_type,
                    (
                        SELECT 
                            count(id) 
                        FROM crm_lead
                        WHERE 
                            extract(month from create_date) = enquiry_date_month
                            AND extract(year from create_date) = enquiry_date_year
                            AND "enquiryType" = m.enquiry_type
                    ) AS enquiry_count,
                    (
                        SELECT 
                            count(e.id) 
                        FROM bb_estimate_estimate e
                        INNER JOIN crm_lead l on l.id = e.lead
                        WHERE 
                            extract(month from e.create_date) = enquiry_date_month
                            AND extract(year from e.create_date) = enquiry_date_year
                            AND l."enquiryType" = m.enquiry_type
                    ) AS enquiry_converted_count,
                    (
                        SELECT 
                            count(s.id) 
                        FROM sale_order s
                        INNER JOIN bb_estimate_estimate e on s."Estimate" = e.id
                        INNER JOIN crm_lead l on l.id = e.lead
                        WHERE 
                            extract(month from s.create_date) = enquiry_date_month
                            AND extract(year from s.create_date) = enquiry_date_year
                            AND l."enquiryType" = m.enquiry_type
                    ) AS enquiry_order_count
                    FROM
                    (
                        SELECT
                            min(id) AS id,
                            extract(month from create_date) AS enquiry_date_month,
                            extract(year from create_date) AS enquiry_date_year,
                            to_char(create_date, 'MM') AS enquiry_month_desc,
                           "enquiryType" AS enquiry_type
                        FROM
                            crm_lead
                        where 
                            "typeOfLead" = 'Bespoke'
                        GROUP BY
                            extract(month from create_date),
                            extract(year from create_date),
                            to_char(create_date, 'MM'),
                            "enquiryType"
                    ) m
                ) f
        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))


class ConversionRatesByMonth(models.Model):
    _name = 'bb_estimate.conversion_rates_months'
    _desc = 'Conversion By Month'
    _auto = False
    _rec_name = 'Year'
    _order = "Year, Month"

    Year = fields.Char('Year', readonly=True)
    Month = fields.Selection([('01','January'), ('02','February'), ('03','March'), ('04','April'), ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'), ('10','October'), ('11','November'), ('12','December')],string='Month',readonly=True)
    TotalEnquiry = fields.Integer('Total Enquiries',readonly=True)
    ConvertedEnquriy = fields.Integer('Converted To Estimate',readonly=True,group_operator="sum")
    ConvertedEnquriyPercent = fields.Float('Converted To Estimate(%)',readonly=True,group_operator="avg")
    ConvertedOrder = fields.Integer('Converted To Order',readonly=True,group_operator="sum")
    ConvertedOrderPercent = fields.Float('Converted To Order(%)',readonly=True,group_operator="avg")

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        return """
            SELECT
                id,
                enquiry_date_year::text AS "Year",
                enquiry_month_desc as "Month",
                enquiry_count AS "TotalEnquiry",
                enquiry_converted_count as "ConvertedEnquriy",
                (enquiry_converted_count / enquiry_count::float * 100)::integer AS "ConvertedEnquriyPercent",
                enquiry_order_count as "ConvertedOrder",
                (enquiry_order_count / enquiry_count::float * 100)::integer AS "ConvertedOrderPercent"
            FROM
                (
                SELECT
                    id,
                    enquiry_date_month,
                    enquiry_date_year,
                    enquiry_month_desc,
                    (
                        SELECT 
                            count(id) 
                        FROM 
                            crm_lead
                        WHERE 
                            extract(month from create_date) = enquiry_date_month
                            AND extract(year from create_date) = enquiry_date_year
                            AND "typeOfLead" = 'Bespoke'
                    ) AS enquiry_count,
                    (
                        SELECT 
                            count(e.id) 
                        FROM bb_estimate_estimate e
                        INNER JOIN crm_lead l on l.id = e.lead
                        WHERE 
                            extract(month from e.create_date) = enquiry_date_month
                            AND extract(year from e.create_date) = enquiry_date_year
                            AND l."typeOfLead" = 'Bespoke'
                    ) AS enquiry_converted_count,
                    (
                        SELECT 
                            count(s.id) 
                        FROM sale_order s
                        INNER JOIN bb_estimate_estimate e on s."Estimate" = e.id
                        INNER JOIN crm_lead l on l.id = e.lead
                        WHERE 
                            extract(month from s.create_date) = enquiry_date_month
                            AND extract(year from s.create_date) = enquiry_date_year
                            AND l."typeOfLead" = 'Bespoke'
                    ) AS enquiry_order_count
                FROM
                (
                    SELECT
                        min(id) AS id,
                        extract(month from create_date) AS enquiry_date_month,
                        extract(year from create_date) AS enquiry_date_year,
                        to_char(create_date, 'MM') AS enquiry_month_desc
                    FROM
                        crm_lead
                    where 
                        "typeOfLead" = 'Bespoke'
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

class ConversionTimesReport(models.Model):
    _name = 'bb_estimate.conversion_times_report'
    _desc = 'Conversion By Month'
    _auto = False
    _rec_name = 'Year'
    _order = "Year, Month"

    Year = fields.Char('Year', readonly=True)
    Month = fields.Selection([('01','January'), ('02','February'), ('03','March'), ('04','April'), ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'), ('10','October'), ('11','November'), ('12','December')],string='Month',readonly=True)
    EnquiryType = fields.Selection([('Envelope Estimate','Envelope Estimate'),('Print Estimate','Print Estimate')], string='Enquiry Type',readonly=True)
    AvgConversionTime = fields.Float('Average Conversion Time', group_operator="avg")

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        return """
            SELECT
                id,
                enquiry_date_year::text AS "Year",
                enquiry_month_desc AS "Month",
                enquiry_type as "EnquiryType",
                (
                    SELECT 
                        avg(extract(epoch from (
                        e.create_date - l.create_date)) / 3600.0) 
                    FROM 
                        crm_lead l
                    INNER JOIN bb_estimate_estimate e ON e.lead = l.id
                    WHERE 
                        extract(month from l.create_date) = enquiry_date_month
                        AND extract(year from l.create_date) = enquiry_date_year
                        AND enquiry_type = m.enquiry_type
                ) AS "AvgConversionTime"
            FROM
                (
                    SELECT
                        min(id) AS id,
                        extract(month from create_date) AS enquiry_date_month,
                        extract(year from create_date) AS enquiry_date_year,
                        to_char(create_date, 'MM') AS enquiry_month_desc,
                        "enquiryType" as enquiry_type
                    FROM
                        crm_lead
                    WHERE
                        "typeOfLead" = 'Bespoke'
                    GROUP BY
                        extract(month from create_date),
                        extract(year from create_date),
                        to_char(create_date, 'MM'),
                        "enquiryType"
                ) m
        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))