function changeField(field_name="") {
    if (field_name === ""){
        field_name = $("#search_term").val();
        $('#search_term').val("");
    }
    $('#terms-container').html('').load(
        "/change_terms", "field=" + field_name
    );
}