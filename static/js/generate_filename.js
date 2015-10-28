$.when(
    $.getScript( "static/js/generate_alfresco_filename.js" ),
    $.getScript( "static/js/generate_activiti_filename.js" ),
    $.Deferred(function( deferred ){
        $( deferred.resolve );
    })
).done(function(){

    //place your code here, the scripts are all loaded
    $(document).ready(function(){
        $("#tabSwitcher li.active a").trigger('click');
    });

});


$("#tabSwitcher li a").click(function(){
    tab_selected = $(this).text();
    
    if(tab_selected.indexOf("Alfresco") > -1) {
        //Alfresco tab selected
        //Based on some business logic, correctly pre-populate the filename field.            
        generate_alfresco_filename();
        
    }
    else if(tab_selected.indexOf("Activiti") > -1) {
        //Activiti tab selected
        generate_activiti_filename();
    }

});

