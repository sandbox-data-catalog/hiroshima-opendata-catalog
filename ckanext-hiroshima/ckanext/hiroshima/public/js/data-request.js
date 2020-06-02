$(function() {
    $("#add-request-form").click(function() {
        var requestForms = $('#request-forms')
        var q_no = requestForms.children().length + 1;

        requestForms.append('<div id="request-form-'+ q_no +'" q_no="' + q_no + '" class="row flex request-form-row"></div>');
        var createdRow = $('#request-form-' + q_no)

        createdRow.append('<div class="col-md-1 label-item_name"><label class="control-label" for="field-item_name">Q' + q_no +'</label></div>');
        createdRow.append('<div class="col-md-6 input-item_name"><input type="text" name="item_name[]" class="form-control field-item_name"></div>');
        createdRow.append('<div class="col-md-1 label-is_require"><label class="control-label" for="field-is_require_' + q_no + '">必須</label></div>');
        createdRow.append('<div class="col-md-1 input-is_require"><input type="checkbox" id="field-is_require_' + q_no + '" name="is_require[]" class="form-control field-is_require"></div>');
        createdRow.append('<div class="col-md-2"><input type="button" class="btn btn-danger delete-request-form" value="削除"></div>');
    });

    $('#request-forms').on('click', '.delete-request-form' , function() {

        var rowCount = $('#request-forms').children().length;
        var deleteRow = $(this).closest('.request-form-row')
        var deleteNo = parseInt(deleteRow.attr('q_no'));
        deleteRow.remove();

        for (var afterNo = deleteNo; afterNo < rowCount; afterNo++) {
            var beforeNo = afterNo + 1;
            var row = $('#request-form-' + beforeNo);
            row.attr('id', 'request-form-' + afterNo );
            row.attr('q_no', afterNo );
            row.find('.label-item_name').children('label').text('Q' + afterNo );
            row.find('.label-is_require').children('label').attr('for', 'field-is_require_' + afterNo );
            row.find('.input-is_require').children('input').attr('id', 'field-is_require_' + afterNo );
        }
    });
});