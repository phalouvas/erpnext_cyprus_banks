# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import base64
import requests

class Settings(Document):

	def onload(self):
		return
		if (get_token(self) == False):
			frappe.throw("Cannot connect")

	pass

def get_base_url(settings):
	return "https://sandbox-oauth.hellenicbank.com" if settings.is_sandbox else "https://oauthprod.hellenicbank.com"

def get_token(settings):
	url = get_base_url(settings) + "/token/exchange"
	payload = {
		"grant_type": "authorization_code",
		"redirect_uri": frappe.local.request.url,
		"code": settings.code
	}
	string_to_encode = settings.client_id + ':' + settings.client_secret
	headers = {
		"Authorization": "Basic " + base64.b64encode(string_to_encode.encode("utf-8")).decode("utf-8")
		
	}

	response = requests.post(url, data=payload, headers=headers)
	response_json = response.json()
	if (response_json.error):
		return False
	frappe.db.set_value('Settings', settings.name, 'authorization_code', response_json)

	pass