import frappe
import json

from frappe import _

def get_context(context):
    if frappe.session.user == 'Guest':
        frappe.local.flags.redirect_location = '/'
        raise frappe.Redirect

    context.user = frappe.session.user
    context.csrf_token = frappe.sessions.get_csrf_token()

    context.employee = frappe.db.get_value("Employee", {"user_id": context.user}, "name") or ""
    context.holiday_list = frappe.db.get_value("Employee", {"user_id": context.user}, "holiday_list") or ""

    valid_roles = ['Leave Approver']
    
    if not('Leave Approver' in frappe.get_roles() or 'HR Manager' in frappe.get_roles()):
        frappe.throw(_('Only users with {0} role can access').format(', '.join(valid_roles)),
			frappe.PermissionError)
    
    allow_delete_leave_history = 0
    allow_cancel_leave_history = 0
    is_hr_manager = 0

    if 'HR Manager' in frappe.get_roles():
        # allow_delete_leave_history = 1
        allow_cancel_leave_history = 1
        is_hr_manager = 1
        
    context.allow_delete_leave_history = allow_delete_leave_history
    context.allow_cancel_leave_history = allow_cancel_leave_history
    context.is_hr_manager = is_hr_manager
    
    context.leave_requests = frappe.db.sql("""
		select la.*, f.file_name, f.file_url
        from `tabLeave Application` la
        left join `tabFile` f on f.attached_to_doctype = "Leave Application" and f.attached_to_name = la.name
		where la.docstatus = 0 and la.leave_approver = %(user)s
	""",{
        "user": frappe.session.user
    }, as_dict=True, debug=1)

    condition_history = "la.docstatus = 1"

    if not is_hr_manager:
        condition_history += " and la.leave_approver = '{0}'".format(frappe.session.user)

    context.leave_historys = frappe.db.sql("""
		select la.*, f.file_name, f.file_url
        from `tabLeave Application` la
        left join `tabFile` f on f.attached_to_doctype = "Leave Application" and f.attached_to_name = la.name
		where {0}
	""".format(condition_history), as_dict=True, debug=1)

    context.list_employee = frappe.db.get_all("Employee",fields=["name", "employee_name"])
    context.list_leave_type = frappe.db.get_all("Leave Type",fields=["name"])
    context.list_leave_status = ["Open","Approved","Rejected","Cancelled"]

    return context