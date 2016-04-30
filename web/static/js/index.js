        $(document).ready(function () {
            // initialize the viewer
            $('#runajax').click(function (event) {
                //sendForm()                
                //var dataToSend = JSON.stringify(params);
                var valueForInput1 = $("#input1").val();
                var valueForInput2 = $("#input2").val();
                var data =
                {
                    key1: valueForInput1,
                    key2: valueForInput2
                };
                var dataToSend = JSON.stringify(data);
                $.ajax(
                        {
                            url: '/schedule',
                            type: 'POST',
                            data: dataToSend,
                            success: function (jsonResponse) {
                                var objresponse = JSON.parse(jsonResponse);
                                console.log(objresponse['newkey']);
                                $("#responsefield").text(objresponse['newkey']);
                            },
                            error: function () {
                                $("#responsefield").text("Error to load api");
                            }
                        });
                event.preventDefault();
            });
        });
