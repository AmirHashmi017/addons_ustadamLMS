from odoo import api, models


class LoanDetails(models.AbstractModel):
    """fetch pdf report values"""
    _name = 'report.tamang_loan_management.loan_report_template'

    @api.model
    def _get_report_values(self, doc_ids, data=None):
        loan_id = self.env['loan.request'].browse(doc_ids)
        data = {
            'Loan_id': loan_id.id,
            'Customer': loan_id.partner_id.name,
            'CustomerAddress': f"{loan_id.partner_id.street} "
                               f"{loan_id.partner_id.city}" if loan_id.partner_id.city
            else '',
            'CustomerAddress2': f"{loan_id.partner_id.city}, "
                                f"{loan_id.partner_id.state_id.name}" if
            loan_id.partner_id.city and loan_id.partner_id.state_id.name
            else '',
            'CustomerContact': loan_id.partner_id.phone,
            'Loan_Type': loan_id.loan_type_id.name,
            'Tenure': loan_id.tenure,
            'Tenure_type': loan_id.loan_type_id.tenure_plan,
            'Interest_Rate': str(loan_id.interest_rate),
            'Loan_Amount': str(loan_id.loan_amount),
        }
        """Fetching values for the report using query and returns the value"""
        query = """SELECT name as Name, date as Date, amount as Amount,
         interest_amount as Interest_amount,state as State, 
         total_amount as Total_amount FROM repayment_line"""
        check = """WHERE"""
        condition = """loan_id='{cust}'""".format(cust=loan_id.id)
        query = """{} {} {}""".format(query, check, condition)
        self.env.cr.execute(query)
        record = self.env.cr.dictfetchall()
        record_sort = sorted(record, key=lambda x: x['date'])
        return {
            'docs': record_sort,
            'doc_ids': doc_ids,
            'data': data,
        }
