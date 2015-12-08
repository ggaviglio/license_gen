function generate_activiti_filename() {

    $( "#activiti_tab input[name*='holder_name'], #activiti_tab input[name*='version'], #activiti_tab #tag_extension" ).change(function() {
        
        var holder_name = $( "#activiti_tab input[name*='holder_name']" ).val().replace(/[^a-zA-Z0-9]+/g, '')        
        var version = $( "#activiti_tab [name*='field_version'] option:selected" ).text()

        var extension = function() {
            if ($('#activiti_tab #tag_extension').prop('checked')) {
                return "-temp"
            } else {
                return ""
            }
        }

        $( "#activiti_tab input[name*='output_filename']" ).val("Activiti-" + version + "-" + holder_name + extension() + ".lic")

    }).change();
}
