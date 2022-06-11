# NMake Makefile portion for code generation and
# intermediate build directory creation
# Items in here should not need to be edited unless
# one is maintaining the NMake build files.

# Create the build directories
vs$(VSVER)\$(CFG)\$(PLAT)\asprintf	\
vs$(VSVER)\$(CFG)\$(PLAT)\gettextlib	\
vs$(VSVER)\$(CFG)\$(PLAT)\gettextlib\libxml	\
vs$(VSVER)\$(CFG)\$(PLAT)\gettextpo	\
vs$(VSVER)\$(CFG)\$(PLAT)\gettextsrc	\
vs$(VSVER)\$(CFG)\$(PLAT)\gettext-runtime-tools	\
vs$(VSVER)\$(CFG)\$(PLAT)\gettext-tools-tools	\
vs$(VSVER)\$(CFG)\$(PLAT)\gnu	\
vs$(VSVER)\$(CFG)\$(PLAT)\grt	\
vs$(VSVER)\$(CFG)\$(PLAT)\intl-runtime	\
vs$(VSVER)\$(CFG)\$(PLAT)\libgrep	\
vs$(VSVER)\$(CFG)\$(PLAT)\libtextstyle	\
vs$(VSVER)\$(CFG)\$(PLAT)\libtextstyle\libxml:
	@-md $@
