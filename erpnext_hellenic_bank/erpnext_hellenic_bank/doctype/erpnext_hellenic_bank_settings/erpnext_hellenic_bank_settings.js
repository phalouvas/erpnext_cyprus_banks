// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Erpnext Hellenic Bank Settings', {
	refresh: function (frm) {

		frm.add_custom_button(__('Authorize'), function () {
			let urlParams = new URLSearchParams(window.location.search);
			if (urlParams.get('state') === null) {
				let is_sandbox = frm.get_field('is_sandbox').value;
				let base_url = is_sandbox ? "https://sandbox-oauth.hellenicbank.com" : "https://oauthprod.hellenicbank.com";
				let client_id = frm.get_field('client_id').value;
				let client_secret = frm.get_field('client_secret').value;
				let href = base_url + "/oauth2/auth?response_type=code&client_id=" + client_id +
					"&redirect_uri=" + window.location.href +
					"&scope=b2b.account.details,b2b.credit.transfer.mass,b2b.account.list,b2b.report.account.statements,b2b.credit.transfer.cancel,b2b.report.credit.transfer.single,b2b.credit.transfer.single,b2b.funds.availability,b2b.report.credit.transfer.mass" +
					"&state=erpnext_state_b64_encoded";
				window.location.href = href;
				frappe.validated = true;
			}
		});

		let urlParams = new URLSearchParams(window.location.search);
		let new_code = urlParams.get('code');
		if (new_code !== null) {
			frappe.db.get_single_value('Erpnext Hellenic Bank Settings', 'code')
				.then(function (old_code) {
					if ((urlParams.get('state') === "erpnext_state_b64_encoded") && (new_code !== old_code)) {
						frappe.db.set_value('Erpnext Hellenic Bank Settings', '', 'code', urlParams.get('code'))
							.then(r => {
								let doc = r.message;
								frappe.call({
									method: "erpnext_hellenic_bank.erpnext_hellenic_bank.doctype.erpnext_hellenic_bank_settings.erpnext_hellenic_bank_settings.get_authorization_code",
									args: {
										// your arguments here
									},
									callback: function(response) {
										if ('error' in response.message) {
											frappe.msgprint(response.message.error);
										} else {
											frappe.msgprint("You succesfully received a new authorization code.");
										}
									}
								});								
							})
					}
				});
		}

	}
});
