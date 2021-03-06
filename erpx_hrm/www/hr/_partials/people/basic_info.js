$(document).ready(function(){
    var old_name = $('#old_name').val();     
    $("#btn-save-employee").click(function () {
        var old_name = $('#old_name').val();    
    
        var args = {};
        var fields = [
            "naming_series",
            "alternate_staff_id",
            "first_name",
            "last_name",
            "preferred_name",
            "designation",
            "personal_email",
            "cell_number",
            "reports_to",
            "department",
            "employment_type",
            "gender",
            "branch",
            "date_of_joining",
            "date_of_birth"
        ]
        $.each(fields, function (key, element) {			        
            args[element] = $(`#divBasicInfo [data-fieldname="${element}"]`).val();   						
        });    
    
        var url = '/api/resource/Employee';    
        var type = 'POST';    
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
                    if(old_name != '')              
                        location.reload();
                    else
                        window.location = 'people.html?name=' + r.data.name;
                }
            }
        });
    });
});