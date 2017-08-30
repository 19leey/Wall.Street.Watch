<!--

// function to update watchlist information
function updateWatchlilst(){
    $.get('/updateWatchlist' ,function (response, status) {
        if (status == 'success') {
            var data = [];
            var stocks = JSON.parse(response);

            for (i in stocks) {
                var stock = stocks[i].StockSymbol+"\">"+stocks[i].StockSymbol + "</a> " + stocks[i].LastTradePrice + " " + stocks[i].Change + " " + stocks[i].ChangePercent + "%<br>";
                data.push('<li class="list-group-item"><a href="/stock/'+stock+'</li>');
                $("#inital").remove();
            }
            $("#list").empty().html(data.join(" "));
        }
    });
}

// function to format json string passed in 
function format(data){
    var jsonObj = JSON.parse(data);
    data = 
        "Symbol: " + jsonObj[0].StockSymbol 
        + "<br>Last Trade Price: " + jsonObj[0].LastTradePrice 
        + "<br>Loss/Gain: " + jsonObj[0].Change 
        + "<br>Loss/Gain Percentage: " + jsonObj[0].ChangePercent + "%"
        + "<br>Last Trade Time: " + jsonObj[0].LastTradeDateTimeLong;

    return data;
}

// function to update stock information every 3 seconds
function updateStock(){
    $.get('/updateStock/{{ ticker }}' ,function (response, status) {
        if (status == 'success')        
            $('#variableInfo').html(format(response));
    });
}

//-->