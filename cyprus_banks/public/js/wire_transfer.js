frappe.ui.form.on('Payment Entry', {
    refresh: function (frm) {
        frm.add_custom_button(__('Wire Transfer'), function () {
            if (
                frm.doc.payment_type == "Pay" &&
                frm.doc.bank_account &&
                frm.doc.party_bank_account &&
                frm.doc.paid_amount &&
                frm.doc.reference_no &&
                frm.doc.reference_date &&
                frm.doc.party_name
            ) {
                frappe.call({
                    method: "cyprus_banks.cyprus_banks.doctype.hellenic_bank.hellenic_bank.single_payment",
                    args: {
                        bank_account: frm.doc.bank_account,
                        party_bank_account: frm.doc.party_bank_account,
                        paid_amount: frm.doc.paid_amount,
                        reference_no: frm.doc.reference_no,
                        reference_date: frm.doc.reference_date,
                        party_name: frm.doc.party_name
                    },
                    callback: function (response) {
                        if (response.message.errors === null) {
                            frappe.msgprint("You succesfully executed the payment.");
                        } else {
                            frappe.msgprint("Something went wrong.", 'Error');
                        }
                    }
                });
            } else {
                frappe.msgprint("Payment type must by Pay, and are required Bank Account, Party Bank Account, Paid Amount, Reference No and Reference Date.", 'Warning');
            }       
        }, "Hellenic Bank");

        frm.add_custom_button(__('Authorize'), function () {
			frappe.set_route('Form', 'Hellenic Bank');
		}, "Hellenic Bank");
    }
});
