var 	irc = document.createElement("iframe");
		irc.id = "irc";
		irc.src = "https://demo.thelounge.chat/?channels=lqdn-travail&nick=anon";

		irc.start = function()
		{
			document.body.appendChild(irc);
		}
