from pathlib import Path
import requests, sys, re

#check the input params
if len(sys.argv) != 2:
	sys.exit('The folder where to find the gradle wrapper configuration is needed')

folder = sys.argv[1]

#take gradle version from wrapper
gradlew_file_path = "{}gradle-wrapper.properties".format(folder)

txt = Path(gradlew_file_path).read_text()
txt = txt.split("gradle-", 1)
gradle_version = txt[1][:3]

#look for java version of the gradle_version
url = 'https://docs.gradle.org/current/userguide/compatibility.html'
r = requests.get(url)
page = r.text

#look for java version inside gradle page
output = re.findall("<td.*>(\d*?|\d.\d*?)<\/p><\/td>", page)

gradle_versions = output[1::2]
java_versions = output[::2]

result = java_versions[gradle_versions.index(str(gradle_version))]

#output for github action
print(f"::set-output name=java-version::{result}")
