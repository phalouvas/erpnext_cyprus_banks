from . import __version__ as app_version

app_name = "cyprus_banks"
app_title = "ERPNext Cyprus Banks"
app_publisher = "KAINOTOMO PH LTD"
app_description = "ERPNext Cyprus Banks Integration"
app_email = "info@kainotomo.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/cyprus_banks/css/cyprus_banks.css"
# app_include_js = "/assets/cyprus_banks/js/cyprus_banks.js"

# include js, css files in header of web template
# web_include_css = "/assets/cyprus_banks/css/cyprus_banks.css"
# web_include_js = "/assets/cyprus_banks/js/cyprus_banks.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "cyprus_banks/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Bank Reconciliation Tool": "public/js/bank_reconciliation_tool.js",
    "Payment Entry": "public/js/wire_transfer.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "cyprus_banks.utils.jinja_methods",
#	"filters": "cyprus_banks.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "cyprus_banks.install.before_install"
# after_install = "cyprus_banks.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "cyprus_banks.uninstall.before_uninstall"
# after_uninstall = "cyprus_banks.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "cyprus_banks.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"cyprus_banks.tasks.all"
#	],
#	"daily": [
#		"cyprus_banks.tasks.daily"
#	],
#	"hourly": [
#		"cyprus_banks.tasks.hourly"
#	],
#	"weekly": [
#		"cyprus_banks.tasks.weekly"
#	],
#	"monthly": [
#		"cyprus_banks.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "cyprus_banks.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "cyprus_banks.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "cyprus_banks.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["cyprus_banks.utils.before_request"]
# after_request = ["cyprus_banks.utils.after_request"]

# Job Events
# ----------
# before_job = ["cyprus_banks.utils.before_job"]
# after_job = ["cyprus_banks.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"cyprus_banks.auth.validate"
# ]
