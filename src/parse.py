import json
import re
import sys

from bs4 import BeautifulSoup
from bs4.element import NavigableString


def main(source, base_url="https://www.gov.si"):
	features = []
	with open(source, "r") as f:
		content = "\n".join(list(f))
	soup = BeautifulSoup(content, features="html.parser")
	for item in soup.select("ul.organisation-list li.list-item"):
		google_link = item.find_all("a", href=re.compile("google.com"))[0]
		coords = []
		props = {}
		if google_link:
			href = google_link["href"]
			coords = [float(n) for n in reversed(href.split("/")[-2].split(","))]
			props["map_link"] = href
		name_h3 = item.find("h3")
		if name_h3:
			props["name"] = name_h3.text.strip()
			if name_h3.a:
				props["link"] = "{}{}".format(base_url, name_h3.a["href"])
		address_p = item.select("div.contact-info p")
		if len(address_p) == 1:
			props["address"] = ", ".join([n.strip() for n in item.select("div.contact-info p")[0] if isinstance(n, NavigableString)])
		phone_link = item.find("a", href=re.compile("tel:.*"))
		if phone_link:
			props["phone_number"] = phone_link.text
			props["phone_number_href"] = phone_link["href"]
		email_link = item.find("a", href=re.compile("mailto:.*"))
		if email_link:
			props["email"] = email_link.text
			props["email_href"] = email_link["href"]
		data = {
			"type": "Feature",
			"geometry": {
				"type": "Point",
				"coordinates": coords
			},
			"properties": props
		}
		if coords and props:
			features.append(data)
	return {
		"type": "FeatureCollection",
		"features": features
	}
	

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: {} [filename]".format(__file__))
	source = sys.argv[1]
	data = main(source)
	print(json.dumps(data, sort_keys=True, indent=4))
	
