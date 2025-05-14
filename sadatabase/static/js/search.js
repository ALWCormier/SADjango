function changeField(field_name="") {
    if (field_name === ""){
        field_name = $("#search_term").val();
        $('#search_term').val("");
    }
    let inputs = $(".termsInput");

    $.ajax({
        url: '/update_field_defaults',
        data: {"field": field_name, "valslist": inputs.serialize()},
        success: function(data) {
            $('#terms-container').html('').load("/change_terms");
        }
    });


}

function detail_table(app_id) {
    $('#detail_table').html('').load(
        "/detail", "app_id=" + app_id
    ); }

function detail_edit(app_id) {
    $("#dataModal").modal("hide");
    $('#edit_table').html('').load(
        "/edit", "app_id=" + app_id
    );
    $("#editModal").modal("show");
    $("#pass_id").val(app_id);
}