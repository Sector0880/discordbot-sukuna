version = {
	"number": "0.9.1.1",
	"name": "Febrephosten"
}


languages = ["ru", "uk"]


avatar = "https://cdn.discordapp.com/attachments/817116435351863306/825447378105925672/avatarNexus.gif"
#avatar = "./botConfiguration/.db/bot/avatars/avatarNexus.jpeg"


colors = [
	{
		"0x": [
			{
				"bot": [
					{
						"black": 0x000001
					},
					{
						"white": 0xfffffe
					}
				]
			},
			{
				"marks": [
					{
						"success": 0x00ce00
					},
					{
						"error": 0xce0000
					}
				]
			}
		]
	},
	{
		"rgb": [
			{
				"bot": [
					{
						"black": (0, 0, 1)
					},
					{
						"white": (255, 255, 255)
					}
				]
			},
			{
				"marks": [
					{
						"success": (0, 206, 0)
					},
					{
						"error": (206, 0, 0)
					}
				]
			}
		]
	}
]

colors_bot = [
	colors[0]["0x"][0]["bot"][0]["black"],
	colors[0]["0x"][0]["bot"][1]["white"]
]

color_success = colors[0]["0x"][1]["marks"][0]["success"]
color_error = colors[0]["0x"][1]["marks"][1]["error"]


#emoji = {
	#"marks": {
		#"success": "<a:mark_success:815121118741659668>",
		#"error": "<a:mark_error:815121144016404500>",
		#"none": "<a:mark_none:815121643479236618>"
	#},
	#"switchs": {
		#"on": "<:switch_on:818125506309652490>",
		#"off": "<:switch_off:818125535951323177>"
	#},
	#"locks": {
		#"unlock": ":unlock:",
		#"lock": ":lock:"
	#},
	#"load": {
		#"ok": "<a:load_ok:815125554553815080>",
		#"partial-lag": "<a:load_partial_lag:815125594396164136>",
		#"lag": "<a:load_lag:815125652319371265>",
		#"none": "<a:load_none:815125685907226654>"
	#},
	#"db": {
		#"ok": "<:db_ok:815122520411865119>",
		#"rework": "<:db_rework:815123566462107679>"
	#}
#}
emoji = [
	{
		"marks": [
			{
				"success": "<a:mark_success:815121118741659668>"
			},
			{
				"error": "<a:mark_error:815121144016404500>"
			},
			{
				"none": "<a:mark_none:815121643479236618>"
			}
		]
	},
	{
		"switchs": [
			{
				"on": "<:switch_on:818125506309652490>"
			},
			{
				"off": "<:switch_off:818125535951323177>"
			}
		]
	},
	{
		"locks": [
			{
				"unlock": ":unlock:"
			},
			{
				"lock": ":lock:"
			}
		]
	},
	{
		"load": [
			{
				"ok": "<a:load_ok:815125554553815080>"
			},
			{
				"partial-lag": "<a:load_partial_lag:815125594396164136>"
			},
			{
				"lag": "<a:load_lag:815125652319371265>"
			},
			{
				"none": "<a:load_none:815125685907226654>"
			}
		]
	},
	{
		"db": [
			{
				"ok": "<:db_ok:815122520411865119>"
			},
			{
				"rework": "<:db_rework:815123566462107679>"
			}
		]
	}
]

emoji_mark_success = emoji[0]["marks"][0]["success"]
emoji_mark_error = emoji[0]["marks"][1]["error"]
emoji_mark_none = emoji[0]["marks"][2]["none"]

emoji_switch_on = emoji[1]["switchs"][0]["on"]
emoji_switch_off = emoji[1]["switchs"][1]["off"]

emoji_lock_unlock = emoji[2]["locks"][0]["unlock"]
emoji_lock_lock = emoji[2]["locks"][1]["lock"]

emoji_load_ok = emoji[3]["load"][0]["ok"]
emoji_load_partial_lag = emoji[3]["load"][1]["partial-lag"]
emoji_load_lag = emoji[3]["load"][2]["lag"]
emoji_load_none = emoji[3]["load"][3]["none"]

emoji_db_ok = emoji[4]["db"][0]["ok"]
emoji_db_rework = emoji[4]["db"][1]["rework"]