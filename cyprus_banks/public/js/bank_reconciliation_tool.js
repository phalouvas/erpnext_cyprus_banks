frappe.ui.form.on('Bank Reconciliation Tool', {
    refresh: function (frm) {
        frm.add_custom_button('Retrieve Bank Transactions', function () {
            if (
                frm.doc.bank_account &&
                frm.doc.bank_statement_from_date &&
                frm.doc.bank_statement_to_date
            ) {
                frappe.call({
                    method: "cyprus_banks.cyprus_banks.doctype.hellenic_bank.hellenic_bank.get_bank_transactions",
                    args: {
                        bank_account: frm.doc.bank_account,
                        bank_statement_from_date: frm.doc.bank_statement_from_date,
                        bank_statement_to_date: frm.doc.bank_statement_to_date
                    },
                    callback: function (response) {
                        if (response.message.errors === null) {
                            frappe.msgprint("You succesfully retrieved the bank transactions.");
                        } else {
                            frappe.msgprint("Something went wrong.", 'Error');
                        }
                    }
                });
            } else {
                frappe.msgprint("Bank Account, From Date and To Date are required.", 'Warning');
            }       
        });
    }
});