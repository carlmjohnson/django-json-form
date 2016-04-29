$(document).ready(function() {
    var bindContainer = (function($container){
        return (function(data) {
            // So we can manipulate the last loaded data from the console
            window.data = data;

            $container.html(data.html);

            $container.find("form[ajax=true]").submit(function(e) {

                e.preventDefault();
                var $this = $(this);

                var form_data = $this.serialize();
                var form_url = $this.attr("action");
                var form_method = $this.attr("method").toUpperCase();

                $.ajax({
                    url: form_url,
                    dataType: "json",
                    type: form_method,
                    data: form_data,
                    cache: false,
                    success: bindContainer($this)
                });
            });
        });
    });

    $("[data-ajax-url]").each(function(){
        var $el = $(this);

        $.ajax({
            dataType: "json",
            url: $el.data("ajax-url"),
            success: bindContainer($el)
        });
    });
});
