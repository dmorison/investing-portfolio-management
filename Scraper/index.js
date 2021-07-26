const axios = require('axios');
const fs = require('fs');

const stocklist = require('./stockList');

const oneDay = 86400;
const oneWeek = 604800;
const oneMonth = 2629743;
let endDate = Date.now();
let startDate = endDate - oneMonth;
endDate = Math.floor(endDate/1000);
startDate = endDate - oneMonth;
console.log(startDate);
console.log(endDate);

async function dataFeed(ticker, company) {
    try {
        const apifeed = await axios.get(`https://query1.finance.yahoo.com/v7/finance/download/${ticker}?period1=${startDate}&period2=${endDate}&interval=1d&events=history&includeAdjustedClose=true`);
        const apidata = apifeed.data;
        
        console.log(apidata);

        fs.writeFile(`./data_feed/${company}.csv`, apidata, function (err) {
            if (err) return console.log(err);
            console.log('success');
        });

    } catch (error) {
        console.log(error);
    }
}

const stocks = stocklist.stocks;
// test.forEach(e => dataFeed(e, true));

for (const symbol of stocks) {
    const file_name = symbol.split('.')[0];
    console.log(symbol);
    console.log(file_name);

    dataFeed(symbol, file_name);
}

const index_symbls = stocklist.index_symbls;
const index_names = stocklist.index_names;
let count = 0;
for (const symbol of index_symbls) {
    const file_name = index_names[count];
    console.log(symbol);
    console.log(file_name);

    dataFeed(symbol, file_name);
    count++;
}
