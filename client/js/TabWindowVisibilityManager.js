/*
TabWindowVisibilityManager

@version: 	1.0
@author:	Jonathan Marzullo
@contact: 	jonathanfever@gmail.com

This plugin will listen when switching between browser tabs using the 
HTML5 Visibility API. And will also listen for browser window focus 
and blur events. Add your code to pause and resume when leaving and 
returning to your webpage.

In case you find this class useful (especially in commercial projects)
I am not totally unhappy for a small donation to my PayPal account
jonathanfever@gmail.com

Copyright (c) 2014 Jonathan Marzullo

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
*/

////////////////////////////////////////////
////////////////////////////////////////////
// TabWindowVisibilityManager
;(function ($) {	

// main visibility API function 
// check if current tab is active or not
var vis = (function(){
		var stateKey, 
			eventKey, 
			keys = {
				hidden: "visibilitychange",
				webkitHidden: "webkitvisibilitychange",
				mozHidden: "mozvisibilitychange",
				msHidden: "msvisibilitychange"
		};
		for (stateKey in keys) {
			if (stateKey in document) {
					eventKey = keys[stateKey];
					break;
			}
		}
		return function(c) {
			if (c) document.addEventListener(eventKey, c);
			return !document[stateKey];
		}
})();


$.fn.TabWindowVisibilityManager = function (options) {	

		// define defaults
        var defaults = {
            onFocusCallback: function(){},
            onBlurCallback: function(){}
        };

        var o = $.extend(defaults, options);	
			
		var notIE = (document.documentMode === undefined),
			isChromium = window.chrome;	
       
	    this.each(function() {
				
			
			/////////////////////////////////////////
			// check if current tab is active or not
			vis(function(){
								
				if(vis()){	
					
					  setTimeout(function(){ 
					  
						// tween resume() code goes here	
						o.onFocusCallback();
					  
					},300);		
															
				} else {
				
					// tween pause() code goes here	
					o.onBlurCallback();					
				}
			});
			
			
			/////////////////////////////////////////
			// check if browser window has focus
			if (notIE && !isChromium) {
			
				// checks for Firefox and other  NON IE Chrome versions
				$(window).on("focusin", function () { 
					
					setTimeout(function(){      
						
						// tween resume() code goes here
						o.onFocusCallback();
					  
					},300);
			
				}).on("focusout", function () {
			
					// tween pause() code goes here
					o.onBlurCallback();			
				});
			
			} else {
				
				// checks for IE and Chromium versions
				if (window.addEventListener) {
			
					// bind focus event
					window.addEventListener("focus", function (event) {
					  
						setTimeout(function(){                 
							 
							 // tween resume() code goes here
							 o.onFocusCallback();
						  
						},300);
			
					}, false);
			
					// bind blur event
					window.addEventListener("blur", function (event) {
			
						// tween pause() code goes
						o.onBlurCallback();
			
					}, false);
			
				} else {
			
					// bind focus event
					window.attachEvent("focus", function (event) {
			
						setTimeout(function(){                 
			
							 // tween resume() code goes here
							 o.onFocusCallback();
						  
						},300);
			
					});
			
					// bind focus event
					window.attachEvent("blur", function (event) {
			
						// tween pause() code goes here
						o.onBlurCallback();
			
					});
				}
			}
		});
        // end each

        return this;
}
})(jQuery);