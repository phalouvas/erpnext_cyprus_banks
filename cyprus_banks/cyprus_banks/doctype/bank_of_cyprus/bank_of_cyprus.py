# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json
from datetime import datetime
import uuid

class BankOfCyprus(Document):
	pass

def get_base_url(bank_of_cyprus):
	return "https://sandbox-apis.bankofcyprus.com/df-boc-org-sb/sb/psd2" if bank_of_cyprus.is_sandbox else "https://apis.bankofcyprus.com/df-boc-org-prd/prod/psd2"

def get_subscription_id():
	bank_of_cyprus = frappe.get_doc("Bank Of Cyprus")
	url = get_base_url(bank_of_cyprus) + "/v1/subscriptions"
	token = json.loads(bank_of_cyprus.token)
	payload = {
		"accounts": {
			"transactionHistory": True,
			"balance": True,
			"details": True,
			"checkFundsAvailability": True
		},
		"payments": {
			"limit": 99999999,
			"currency": "string",
			"amount":99999999
		},
			"customerInformation": {
			"personalInformation":True,
			"identification":True,
			"address":True,
			"telephone":True,
			"pepinformation":True,
			"reviewInformation":True
		}
	}
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization": "Bearer " + token["access_token"],
		"originUserId": bank_of_cyprus.user_id,
		"timeStamp": datetime.utcnow().isoformat(),
		"journeyId": str(uuid.uuid4()),
		"app_name": "ERPNext Integration"
	}
	response = requests.post(url, json=payload, headers=headers)
	if (response.status_code != 200):
		return response.json()
	frappe.db.set_value('Bank Of Cyprus', bank_of_cyprus.name, 'subscription_id', response.text)
	return response.json()

@frappe.whitelist()
def get_access_token():
	bank_of_cyprus = frappe.get_doc("Bank Of Cyprus")

	token = json.loads(bank_of_cyprus.token)
	expires_datetime = datetime.fromtimestamp(token["consented_on"] + token["expires_in"])

	if datetime.now() > expires_datetime:
		url = get_base_url(bank_of_cyprus) + "/oauth2/token"
		payload = {
			"grant_type": "client_credentials",
			"scope": "TPPOAuth2Security",
			"client_id": bank_of_cyprus.client_id,
			"client_secret": bank_of_cyprus.get_password("client_secret")
		}
		headers = {
			"Accept": "application/json",
			"Content-Type": "application/x-www-form-urlencoded"
		}
		response = requests.post(url, data=payload, headers=headers)
		if (response.status_code != 200):
			return response.json()
		frappe.db.set_value('Bank Of Cyprus', bank_of_cyprus.name, 'token', response.text)
	
	return get_subscription_id()

	
@frappe.whitelist()
def get_authorization_code(code):
	frappe.throw(code)
