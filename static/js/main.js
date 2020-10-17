$(document).ready(function() {
    $('#image').on('change', function() {
        let fileName = $(this).val();
        let slash = fileName.lastIndexOf('/');
        if (fileName.lastIndexOf('\\') > slash) slash = fileName.lastIndexOf('\\');
        $(this).next('.custom-file-label').text(fileName.substring(slash + 1));
    })
});