var page = new WebPage()
var fs = require('fs');
page.settings.userAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1';
page.settings.resourceTimeout = 300;
var settings = {
  encoding: 'utf8',
};

page.onLoadFinished = function() {
console.log('page load finished');
fs.write('1.html', page.content, 'w');
phantom.exit();
};

page.open('https://www.kayak.es/flights/ROM-MAD/2017-10-11-flexible/2017-10-19-flexible', function() {
page.evaluate(function() {
});
});