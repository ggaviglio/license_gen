function escapeRegExp(string) {
    return string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
}

function replaceAll(string, find, replace) {
    return string.replace(new RegExp(escapeRegExp(find), 'g'), replace);
}

function generate_alfresco_filename() {

    $( "#alfresco_tab input[name*='holder_name'], #alfresco_tab #release_key, #alfresco_tab input[id^='tag_']" ).change(function() {
        var holder_name = $( "#alfresco_tab input[name*='holder_name']" ).val().replace(/[^a-zA-Z0-9]+/g, '')
        var release_key = $( "#alfresco_tab #release_key option:selected" ).text()

        var extension = function(){
            var extension = ""
            $.each($("#alfresco_tab input[id^='tag_']"), function() {
                tag_id = this.id.replace('tag_','')
                if (tag_id == 'extension' && this.checked) {
                    extension = '-temp'
                } 
                else if (tag_id.length > 0 && this.checked) {
                    extension = "-" + replaceAll(tag_id, '_', '-')
                }
            });
            return extension
        }

        $( "#alfresco_tab input[name*='output_filename']" ).val("Alfresco-" + release_key + "-" + holder_name + extension() + ".lic")

    }).change();
}
