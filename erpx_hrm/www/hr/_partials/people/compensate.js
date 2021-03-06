$(document).ready(function(){
    var old_name = $('#old_name').val();     
    $("#btn-save-compensate").click(function () {
        var args = {};
        var fields = [
            "salary_basis",
            "salary_amount",
            "bank_name",
            "bank_ac_no",
            "epf_no",
            "tax_no",
            "zakat_no"
        ]
        $.each(fields, function (key, element) {			        
            args[element] = $(`#divCompensate [data-fieldname="${element}"]`).val();   						
        });    
    
        var url = '/api/resource/Employee';    
        var type = 'POST';
        var old_name = $('#old_name').val();
        if(old_name != ''){
            url += '/' + old_name;
            type = 'PUT';
        }
        frappe.ajax({
            type: type,
            url: url,
            args: args,
            callback: function (r) {
                if (!r.exc_type) {                
                    location.reload();
                }
            }
        });
    });   
});