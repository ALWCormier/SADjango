function setModalInputID(id){var modal = document.getElementById("moveID").value = id;}

function detail_table(app_id) {
    $('#detail_table').html('').load(
        "/detail", "app_id=" + app_id
    ); }

function detail_edit(app_id) {
    console.log("see here") // sanity check
    $("#dataModal").modal("hide");
    $('#edit_table').html('').load(
        "/edit", "app_id=" + app_id
    );
    $("#editModal").modal("show");
    $("#pass_id").val(app_id);
}

