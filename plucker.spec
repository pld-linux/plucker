# TODO: do all post/preun/postun work during package build!
%include	/usr/lib/rpm/macros.python
Summary:	plucker - PalmOS conduit 
Summary(pl):	plucker - ³±cznik z systemem PalmOS
Name:		plucker
Version:	1.4	
Release:	%{relyear}%{relmonth}%{relday}%{relhour}m%{relminute}m%{relsecond}s
License:	GPL
Group:		X11/Aplications
Source0:	http://www.plkr.org/snapshots/%{name}_snapshot.tar.gz
# Source0-md5:	df2c29d380a29bc04550a92a79a1769f
Patch0:         %{name}-pld.patch
URL:		http://www.plkr.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel
BuildRequires:	netpbm-progs
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	wxGTK2-devel
%pyrequires_eq	python
BuildRoot:	%{tmpdir}/%{name}-%{version}-%{release}-root-%(id -u -n)

# This is fuckin' piece of shit made only because plucker's developers 
# seem to no longer make source code tarballs available. Evil.

%define		relyear 	2003
%define		relmonth	09
%define		relday		14
%define 	relhour		12
%define		relminute	01
%define		relsecond	33

%define		release		%{relyear}-%{relmonth}-%{relday}_%{relhour}h%{relminute}m%{relsecond}s

%description
Plucker increases the utility of your handheld device by letting you
view web pages and any document that can be converted to HTML or text.
Plucker has many advanced features including the ability to read web
pages with embedded images, an advanced find function, the ability to
open an e-mail form when tapping on mail-links in web documents, an
impressive compression ratio for the documents and an open, documented
format. It can also be customized for your specific needs.

%description -l pl
Plucker zwiêksza u¿yteczno¶æ palmtopa pozwalaj±c na przegl±danie
stron internetowych i innych dokumentów, które mog± zostaæ
skonwertowane do formatu tekstowego lub HTML. Plucker ma wiele
zaawansowanych mo¿liwo¶ci w³±czaj±c w to mo¿liwo¶æ czytania stron
internetowych z osadzonymi obrazkami, funkcjê zaawansowanego
wyszukiwania, mo¿liwo¶æ uruchomienia klienta poczty dla odpowiednich
linków, imponuj±cy wspó³czynnik kompresji dla dokumentów oraz otwarty,
udokumentowany format. Mo¿e zostaæ tak¿e dostosowany do innych 
specyficznych wymagañ.

%prep
%setup -q -n %{name}_%{release}
#cp %{_sourcedir}/setup.py.in %{_builddir}/%{name}-%{version}
%patch0 -p1

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
cd unix
cat>>pld_install_answers<<EOF
$RPM_BUILD_ROOT
$RPM_BUILD_ROOT/bin
y
$RPM_BUILD_ROOT/usr/share/%{name}
$RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}-%{release}
y
$RPM_BUILD_ROOT/var/spool/netcomics
y
n
y
EOF
./install-plucker < pld_install_answers

%install
rm -rf $RPM_BUILD_ROOT
%define PyPluckerDir %{py_sitedir}/PyPlucker
%define DataDir %{_datadir}/plucker
%define DocDir %{_datadir}/doc/plucker

# Viewer
install -d $RPM_BUILD_ROOT%{DataDir}/palm
install -m 755 viewer/*.prc $RPM_BUILD_ROOT%{DataDir}/palm
install -m 755 viewer/*.pdb $RPM_BUILD_ROOT%{DataDir}/palm

# Python Parser
install -d $RPM_BUILD_ROOT%{PyPluckerDir}/helper
install -m 755 parser/PyPlucker/*.py $RPM_BUILD_ROOT%{PyPluckerDir}
install -m 755 parser/PyPlucker/helper/*.py $RPM_BUILD_ROOT%{PyPluckerDir}/helper

# Config files
install -d $RPM_BUILD_ROOT%{DataDir}/config
install parser/exclusionlist.txt $RPM_BUILD_ROOT%{DataDir}/config
install parser/home.html $RPM_BUILD_ROOT%{DataDir}/config
install parser/pluckerrc.sample $RPM_BUILD_ROOT%{DataDir}/config

install -d $RPM_BUILD_ROOT%{_bindir}
sed -e "s:@VERSION@:%{version}:" \
    -e "s:@PLUCKERDIR@:%{DataDir}:" setup.py.in > setup.py
install -m 755 setup.py $RPM_BUILD_ROOT%{_bindir}/plucker-setup

# Documentation
# TODO: copy only needed files!
install -d manual
cp -rf docs/* manual

install -d $RPM_BUILD_ROOT%{_mandir}/man1
install parser/plucker-build.1 $RPM_BUILD_ROOT%{_mandir}/man1
install parser/plucker-decode.1 $RPM_BUILD_ROOT%{_mandir}/man1
install parser/plucker-dump.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post
python %{_libdir}/python/compileall.py %{PyPluckerDir}
python -O %{_libdir}/python/compileall.py %{PyPluckerDir}

# make sure we don't have some old cruft in the binary dir
rm -f %{_bindir}/plucker-build
rm -f %{_bindir}/plucker-decode
rm -f %{_bindir}/plucker-dump

# add links to parser tools
ln -s %{PyPluckerDir}/Spider.py  %{_bindir}/plucker-build
ln -s %{PyPluckerDir}/PluckerDocs.py %{_bindir}/plucker-decode
ln -s %{PyPluckerDir}/PluckerDecode.py %{_bindir}/plucker-dump

%preun
rm -f %{PyPluckerDir}/*.pyc
rm -f %{PyPluckerDir}/*.pyo
rm -f %{PyPluckerDir}/helper/*.pyc
rm -f %{PyPluckerDir}/helper/*.pyo

%postun
rm -f %{_bindir}/plucker-build
rm -f %{_bindir}/plucker-decode
rm -f %{_bindir}/plucker-dump

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGREPORT CREDITS ChangeLog FAQ NEWS README REQUIREMENTS TODO manual
%attr(755,root,root) %{_bindir}/plucker-setup
%{_mandir}/man1/plucker-build*
%{_mandir}/man1/plucker-decode*
%{_mandir}/man1/plucker-dump*
%{py_sitedir}/PyPlucker
%{_datadir}/plucker
