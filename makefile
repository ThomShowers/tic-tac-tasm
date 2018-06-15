OBJDIR := bld/obj
OBJS := $(OBJDIR)/io.o

TESTPROXYDIR = tests/native
TESTPROXYS = $(TESTPROXYDIR)/io.so

.PHONY : build
build : $(OBJS)

$(OBJDIR)/io.o : win_io.asm | $(OBJDIR)
	nasm -f win32 -o $@ $<

$(TESTPROXYDIR)/io.so : $(OBJDIR)/io.o | $(TESTPROXYDIR)
	link /DLL /EXPORT:println /EXPORT:scanln /EXPORT:cursorUp /NOENTRY /OUT:$(OBJDIR)/io.so $< kernel32.lib
	cp $(OBJDIR)/io.so $(TESTPROXYDIR)

$(OBJDIR) :
	mkdir -p $(OBJDIR)

$(TESTPROXYDIR) :
	mkdir -p $(TESTPROXYDIR)

.PHONY : tests
test : build $(TESTPROXYS)
	powershell ./test.ps1

.PHONY : clean
clean : 
	-rm -r bld
	-rm -r tests/__pycache__
	-rm -r tests/native

