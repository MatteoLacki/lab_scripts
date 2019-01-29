import xml.etree.ElementTree as ET


def extract_params(apex3d):
	tree = ET.parse(apex3d)
	root = tree.getroot()
	params = {}
	for p in root.find('PARAMS'):
		params[p.attrib['NAME']] = p.attrib['VALUE']
	return params


chosen_parameters = ["InputFile", "AcquiredName", "AcquiredDate",\
	"AcquiredTime", "SampleDescription", "ChromFWHM_Min", "msResolution"]
