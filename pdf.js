"use strict";
var page = require('webpage').create(),
system = require('system'),
address, output, size;

if (system.args.length < 3 || system.args.length > 5) {
    console.log('Usage: screenshot.js <URL> <filename>');
    phantom.exit(1);
} else {
    address = system.args[1];
    output = system.args[2];
    page.viewportSize = { width: 1280, height: 900};
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
            phantom.exit();
        } else {
            window.setTimeout(function () {
                page.includeJs("//code.jquery.com/jquery-1.10.1.min.js", function() {
                    var size = page.evaluate(function () {
                        return {width: width = "36cm", height : $(document).height()*2+400 + "px", margin: '0px' };
                    });
                    page.paperSize = size;          
                    page.render(output);
                    phantom.exit();
                });
            }, 400);
        }
    });
}
