$('#first_cat').on('change',function(){

    $.ajax({
        url: "/scatter",
        method: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': document.getElementById('first_cat').value
        },
        // the data type that you expect to get from server
        dataType:"json",
        success: function (data) {
            // here the data it get was the new data after processing 
            // 30 It is because Ajax is asynchronous, the success or the error function will be called later, when the server answer the client.
            // change without reload
            Plotly.newPlot('bargraph', data);
        }
    });
})


$('input[name="radio_sel"]').on('change',function(){

    $.ajax({
        url: "/churn",
        method: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': $("input[name='radio_sel']:checked").val()
        },
        // the data type that you expect to get from server
        dataType:"json",
        success: function (data) {
            // here the data it get was the new data after processing 
            // 30 It is because Ajax is asynchronous, the success or the error function will be called later, when the server answer the client.
            // change without reload
            Plotly.newPlot('bargraph', data);
        }
    });
})


$("input[name='target_sel']").on('change',function(){

    $.ajax({
        url: "/cba",
        method: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': $("input[name='target_sel']:checked").val(),
            'budget': $("input[name='budget_i']").val(),
            'cpm': $("input[name='cpm_i']").val(),  
            'ctr': $("input[name='ctr_i']").val(),  
        },
        // the data type that you expect to get from server
        dataType:"json",
        success: function (data) {
            // here the data it get was the new data after processing 
            // 30 It is because Ajax is asynchronous, the success or the error function will be called later, when the server answer the client.
            // change without reload
            $("input[name='imp_i']").val(data['imp'])
            $("input[name='clicks_i']").val(data['clicks'])
            $("input[name='conv_i']").val(data['convert'])                        
            $("input[name='rev_i']").val(data['rev'])
            $("input[name='profit_i']").val(data['profit'])
            $("input[name='roi_i']").val(data['roi'])
        }
    });
})


$("input[name='budget_i']").on('change',function(){

    $.ajax({
        url: "/cba",
        method: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': $("input[name='target_sel']:checked").val(),
            'budget': $("input[name='budget_i']").val(),
            'cpm': $("input[name='cpm_i']").val(),  
            'ctr': $("input[name='ctr_i']").val(),  
        },
        // the data type that you expect to get from server
        dataType:"json",
        success: function (data) {
            // here the data it get was the new data after processing 
            // 30 It is because Ajax is asynchronous, the success or the error function will be called later, when the server answer the client.
            // change without reload
            $("input[name='imp_i']").val(data['imp'])
            $("input[name='clicks_i']").val(data['clicks'])
            $("input[name='conv_i']").val(data['convert'])                        
            $("input[name='rev_i']").val(data['rev'])
            $("input[name='profit_i']").val(data['profit'])
            $("input[name='roi_i']").val(data['roi'])
        }
    });
})


$("input[name='cpm_i']").on('change',function(){

    $.ajax({
        url: "/cba",
        method: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': $("input[name='target_sel']:checked").val(),
            'budget': $("input[name='budget_i']").val(),
            'cpm': $("input[name='cpm_i']").val(),  
            'ctr': $("input[name='ctr_i']").val(),  
        },
        // the data type that you expect to get from server
        dataType:"json",
        success: function (data) {
            // here the data it get was the new data after processing 
            // 30 It is because Ajax is asynchronous, the success or the error function will be called later, when the server answer the client.
            // change without reload
            $("input[name='imp_i']").val(data['imp'])
            $("input[name='clicks_i']").val(data['clicks'])
            $("input[name='conv_i']").val(data['convert'])                        
            $("input[name='rev_i']").val(data['rev'])
            $("input[name='profit_i']").val(data['profit'])
            $("input[name='roi_i']").val(data['roi'])
        }
    });
})


$("input[name='ctr_i']").on('change',function(){

    $.ajax({
        url: "/cba",
        method: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': $("input[name='target_sel']:checked").val(),
            'budget': $("input[name='budget_i']").val(),
            'cpm': $("input[name='cpm_i']").val(),  
            'ctr': $("input[name='ctr_i']").val(),  
        },
        // the data type that you expect to get from server
        dataType:"json",
        success: function (data) {
            // here the data it get was the new data after processing 
            // 30 It is because Ajax is asynchronous, the success or the error function will be called later, when the server answer the client.
            // change without reload
            $("input[name='imp_i']").val(data['imp'])
            $("input[name='clicks_i']").val(data['clicks'])
            $("input[name='conv_i']").val(data['convert'])                        
            $("input[name='rev_i']").val(data['rev'])
            $("input[name='profit_i']").val(data['profit'])
            $("input[name='roi_i']").val(data['roi'])
        }
    });
})

