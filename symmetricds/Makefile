SYMD_DOWNLOAD_URL=https://sourceforge.net/projects/symmetricds/files/symmetricds/symmetricds-3.8/symmetric-server-3.8.43.zip/download

symmetricds.zip:
	$(if $(shell command -v wget 2> /dev/null),\
		wget -O symmetricds.zip ${SYMD_DOWNLOAD_URL},\
		curl -Lo symmetricds.zip ${SYMD_DOWNLOAD_URL} \
	)
	touch $@

symmetricds: symmetricds.zip
	unzip symmetricds.zip
	mv symmetric-server-3.8.43 symmetricds
	touch $@

# https://stackoverflow.com/a/37197276/1556838
install: symmetricds
	$(if $(shell command -v java 2> /dev/null),$(info Found `java`),$(error Please install `java`))

clean:
	rm -rf symmetricds.zip symmetricds
