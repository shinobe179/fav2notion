prepare:
	mkdir lambda_packages
	poetry run pip3 freeze > requirements.txt
	poetry run pip3 install -r requirements.txt -t lambda_packages
	cp -p *.py lambda_packages
	cd lambda_packages && zip -r ../lambda_packages.zip . && cd ..
	rm -rf lambda_packages/*
	rmdir lambda_packages
	rm requirements.txt

