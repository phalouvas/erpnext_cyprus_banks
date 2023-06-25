# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import base64
import requests
import json
from datetime import datetime

class ErpnextHellenicBankSettings(Document):

	def onload(self):
		return

	pass

def base64_encode(string):
    string_bytes = string.encode('utf-8')  # Convert string to bytes using UTF-8 encoding
    encoded_bytes = base64.b64encode(string_bytes)  # Base64 encode the bytes
    encoded_string = encoded_bytes.decode('utf-8')  # Convert the encoded bytes back to a string
    return encoded_string

def get_base_url_auth(erpnext_hellenic_bank_settings):
	return "https://sandbox-oauth.hellenicbank.com" if erpnext_hellenic_bank_settings.is_sandbox else "https://oauthprod.hellenicbank.com"

def get_base_url_api(erpnext_hellenic_bank_settings):
	return "https://sandbox-apis.hellenicbank.com" if erpnext_hellenic_bank_settings.is_sandbox else "https://apisprod.hellenicbank.com"

@frappe.whitelist()
def get_authorization_code():
	erpnext_hellenic_bank_settings = frappe.get_doc("Erpnext Hellenic Bank Settings")
	url = get_base_url_auth(erpnext_hellenic_bank_settings) + "/token/exchange"
	payload = {
		"grant_type": "authorization_code",
		"redirect_uri": frappe.utils.get_url() + "/app/erpnext-hellenic-bank-settings",
		"code": erpnext_hellenic_bank_settings.code
	}
	string_to_encode = erpnext_hellenic_bank_settings.client_id + ':' + erpnext_hellenic_bank_settings.client_secret
	headers = {
		"Authorization": "Basic " + base64.b64encode(string_to_encode.encode("utf-8")).decode("utf-8")
		
	}

	response = requests.post(url, data=payload, headers=headers)
	if (response.status_code != 200):
		return response.json()
	frappe.db.set_value('Erpnext Hellenic Bank Settings', erpnext_hellenic_bank_settings.name, 'authorization_code', response.text)
	return response.json()

@frappe.whitelist()
def refresh_token():
	erpnext_hellenic_bank_settings = frappe.get_doc("Erpnext Hellenic Bank Settings")
	authorization_code = json.loads(erpnext_hellenic_bank_settings.authorization_code)

	# Check if the token is expired
	now = datetime.now()
	expires_at = datetime.fromtimestamp(authorization_code["expires_at"] / 1000)
	if now > expires_at:
		url = get_base_url_auth(erpnext_hellenic_bank_settings) + "/token"
		payload = {
			"grant_type": "refresh_token",
			"refresh_token": authorization_code["refresh_token"]
		}
		string_to_encode = erpnext_hellenic_bank_settings.client_id + ':' + erpnext_hellenic_bank_settings.client_secret
		headers = {
			"Authorization": "Basic " + base64.b64encode(string_to_encode.encode("utf-8")).decode("utf-8")
		}

		response = requests.post(url, data=payload, headers=headers)
		if (response.status_code != 200):
			return response.json()
		frappe.db.set_value('Erpnext Hellenic Bank Settings', erpnext_hellenic_bank_settings.name, 'authorization_code', response.text)
		return response.json()
	else:
		return authorization_code

@frappe.whitelist()
def create_accounts():
	refresh_token()
	erpnext_hellenic_bank_settings = frappe.get_doc("Erpnext Hellenic Bank Settings")
	authorization_code = json.loads(erpnext_hellenic_bank_settings.authorization_code)
	url = get_base_url_api(erpnext_hellenic_bank_settings) + "/v1/b2b/account/list"
	payload = {}
	headers = {
		"Authorization": "Bearer " + authorization_code["access_token"],
		"x-client-id": erpnext_hellenic_bank_settings.client_id	
	}

	response = requests.get(url, params=payload, headers=headers)
	response_json = response.json()
	if (response.status_code != 200):
		return response_json
	
	accounts = response_json["payload"]["accounts"]
	for account in accounts:
		if not frappe.db.exists('Bank Account', account["accountName"] + " - " + erpnext_hellenic_bank_settings.bank):
			new_account = frappe.get_doc({
				'doctype': 'Account',
				'account_name': account["accountName"],
				'parent_account': erpnext_hellenic_bank_settings.parent_account,
				'account_type': 'Bank',
				'account_currency': account["accountCurrencyCodes"],
			})
			new_account.insert()

			bank_account = frappe.get_doc({
				'doctype': 'Bank Account',
				'account_name': account["accountName"],
				'account': new_account.name,
				'is_company_account': True,
				'bank': erpnext_hellenic_bank_settings.bank,
				'bank_account_no': account["accountNumber"],
				'currency': account["accountCurrencyCodes"],
				'iban': account["iban"],
			})
			bank_account.insert()
			
	return response_json

@frappe.whitelist()
def get_bank_transactions(bank_account, bank_statement_from_date, bank_statement_to_date):

	#make_sample_payment()

	bank_account_doc = frappe.get_doc("Bank Account", bank_account)
	dateFrom = datetime.strptime(bank_statement_from_date, '%Y-%m-%d').strftime('%Y%m%d0000')
	dateTo = datetime.strptime(bank_statement_to_date, '%Y-%m-%d').strftime('%Y%m%d2359')

	refresh_token()
	erpnext_hellenic_bank_settings = frappe.get_doc("Erpnext Hellenic Bank Settings")
	authorization_code = json.loads(erpnext_hellenic_bank_settings.authorization_code)
	url = get_base_url_api(erpnext_hellenic_bank_settings) + "/v1/b2b/account/report"
	payload = {
		"dateTo": dateTo,
		"dateFrom": dateFrom,
		"account": bank_account_doc.iban
	}
	headers = {
		"Authorization": "Bearer " + authorization_code["access_token"],
		"x-client-id": erpnext_hellenic_bank_settings.client_id	
	}

	response = requests.get(url, params=payload, headers=headers)
	response_json = response.json()
	if (response.status_code != 200):
		return response_json
	
	transactions = response_json["payload"]["transactions"]
	for transaction in transactions:
		bank_transaction = frappe.get_doc({
			"doctype": "Bank Transaction",
			"bank_account": bank_account,
			"status": "Pending",
			"date": transaction["transactionValueDate"],
			"reference_number": transaction["customerReference"],
			"description": transaction["paymentNotes"],
		})
		amount = transaction["transactionAmount"]
		if amount > 0:
			bank_transaction.deposit = abs(amount)
		else:
			bank_transaction.withdrawal = abs(amount)

		bank_transaction.insert()
		bank_transaction.submit()
			
	return response_json

def make_sample_payment():
	refresh_token()
	erpnext_hellenic_bank_settings = frappe.get_doc("Erpnext Hellenic Bank Settings")
	authorization_code = json.loads(erpnext_hellenic_bank_settings.authorization_code)
	url = get_base_url_api(erpnext_hellenic_bank_settings) + "/v1/b2b/credit/transfer"
	payload = {
		"executionDate": "2023-06-25",
		"beneficiaryAddress": "Customer Address",
		"amount": "23.90",
		"beneficiaryBankAddress": "Bank Address",
		"beneficiaryCountry": "CY",
		"clearingHouseCode": "",
		"debtorAccount": "CY68005000121234567890123456",
		"beneficiaryAccount": "CY48005000121234504938475123",
		"beneficiaryName": "JOHN DOE",
		"beneficiaryBankCountry": "CY",
		"beneficiaryBankName": "Hellenic Bank",
		"transactionUrgency": "S",
		"currency": "EUR",
		"paymentNotes": "notes",
		"debtorBic": "HEBACY2N",
		"beneficiaryBankBic": "HEBACY2N",
		"intermediaryInstitutionBic": "HEBACY2N",
		"emailConfirmation": "",
		"charges": "O",
		"customerReference": "uniqueValue_5",
		"faxConfirmation": ""
	}
	headers = {
		"Authorization": "Bearer " + authorization_code["access_token"],
		"x-client-id": erpnext_hellenic_bank_settings.client_id,
		'Content-Type': 'application/json'
	}

	response = requests.post(url, json=payload, headers=headers)
	response_json = response.json()
	if (response.status_code != 200):
		return response_json
	return response_json
