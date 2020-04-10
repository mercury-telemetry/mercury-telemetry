SHELL=/bin/bash
SYMD_DOWNLOAD_URL=https://sourceforge.net/projects/symmetricds/files/symmetricds/symmetricds-3.8/symmetric-server-3.8.43.zip/download

PROPERTIES=\
	symmetricds/engines/engine0.properties \
	symmetricds/engines/engine1.properties \

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
install: symmetricds ${PROPERTIES}
	$(if $(shell command -v java 2> /dev/null),$(info Found `java`),$(error Please install `java`))

symmetricds/engines/engine%.properties: symmetricds
	cp template/$(@F) $(@D)/$(@F)

check-properties: ${PROPERTIES}
	@for prop in $+ ; do \
		./check-properties.py $$prop || exit 1 ; \
	done

SYMD_BIN=symmetricds/bin
configure: check-properties
	${SYMD_BIN}/dbsql -e engine0 --sql "" || (echo "Failed to connect to engine0."; exit 1)
	${SYMD_BIN}/dbsql -e engine1 --sql "" || (echo "Failed to connect to engine1."; exit 1)
	${SYMD_BIN}/symadmin -e engine0 create-sym-tables || exit 1
	${SYMD_BIN}/dbimport -e engine0 configure.sql


clean-symd-table:
	-${SYMD_BIN}/symadmin -e engine0 uninstall
	-${SYMD_BIN}/symadmin -e engine1 uninstall

clean: clean-symd-table
	-rm -rf symmetricds.zip symmetricds

.PHONY: clean clean-symd-table configure install check-properties
