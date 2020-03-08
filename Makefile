up:
	docker-compose up


run_tests:
	CURRENT_UID=$(id -u):$(id -g) \
	docker-compose -p some-stuff-tests -f docker-compose-tests.yaml up \
	--abort-on-container-exit