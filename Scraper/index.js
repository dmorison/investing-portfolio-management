const axios = require('axios');
const fs = require('fs');

const oneDay = 86400;
const oneWeek = 604800;
const oneMonth = 2629743;
let endDate = Date.now();
let startDate = endDate - oneMonth;
endDate = Math.floor(endDate/1000);
startDate = Math.floor(startDate/1000);
console.log(startDate);
console.log(endDate);
      
async function dataFeed(ticker) {
    try {
        const apifeed = await axios.get(`https://query1.finance.yahoo.com/v7/finance/download/${ticker}?period1=${startDate}&period2=${endDate}&interval=1d&events=history&includeAdjustedClose=true`);
        const apidata = apifeed.data;
        
        console.log(apidata);

        fs.writeFile(`/data_feed/${ticker}.csv`, apidata, function (err) {
            if (err) return console.log(err);
            console.log('success');
        });

    } catch (error) {
        console.log(error);
    }
}

dataFeed('GOOG');
