.PHONY: all clean translate resources

ROOT_DIR=$(shell pwd)

resources:
	pyrcc5 $(ROOT_DIR)/gmbox_sidebar/resources.qrc -o $(ROOT_DIR)/gmbox_sidebar/resources.py
	pyrcc5 $(ROOT_DIR)/sidebarapps/logout/resources.qrc -o $(ROOT_DIR)/sidebarapps/logout/resources.py
	pyrcc5 $(ROOT_DIR)/sidebarapps/sidebar_settingsa/resources.qrc -o \
																$(ROOT_DIR)/sidebarapps/sidebar_settings/resources.py

clean:
	rm -f $(ROOT_DIR)/resources.py