function getResult(url){
    var result = null;
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        async: false,
        success: function(data){
            result = data;
        }
    });
    // console.log(result);
    return result;
}