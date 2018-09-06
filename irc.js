var 	irc = document.createElement("iframe");
		irc.id = "irc";
		irc.src = "https://demo.thelounge.chat/";	

		irc.start = function()
		{
			document.body.appendChild(irc);
		}
