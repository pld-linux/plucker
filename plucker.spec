# TODO: eliminate BR: python-devel-src
Summary:	plucker - PalmOS conduit 
Summary(pl.UTF-8):	plucker - łącznik z systemem PalmOS
Name:		plucker
Version:	1.8
Release:	0.1
License:	GPL
Group:		X11/Aplications
Source0:	http://downloads.plkr.org/%{version}/%{name}_src-%{version}.tar.bz2
# Source0-md5:	ff4d0890ebdfd1a0f130530b67bafc0b
Patch1:		%{name}-pld.patch
URL:		http://www.plkr.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	gtk+2-devel
BuildRequires:	latex2html
BuildRequires:	libjpeg-devel
BuildRequires:	netpbm-progs
BuildRequires:	pkgconfig
BuildRequires:	python-devel-src
BuildRequires:	python-modules
BuildRequires:	sgml-tools
BuildRequires:	wxGTK2-devel
%pyrequires_eq	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Plucker increases the utility of your handheld device by letting you
view web pages and any document that can be converted to HTML or text.
Plucker has many advanced features including the ability to read web
pages with embedded images, an advanced find function, the ability to
open an e-mail form when tapping on mail-links in web documents, an
impressive compression ratio for the documents and an open, documented
format. It can also be customized for your specific needs.

%description -l pl.UTF-8
Plucker zwiększa użyteczność palmtopa pozwalając na przeglądanie
stron internetowych i innych dokumentów, które mogą zostać
skonwertowane do formatu tekstowego lub HTML. Plucker ma wiele
zaawansowanych możliwości włączając w to możliwość czytania stron
internetowych z osadzonymi obrazkami, funkcję zaawansowanego
wyszukiwania, możliwość uruchomienia klienta poczty dla odpowiednich
linków, imponujący współczynnik kompresji dla dokumentów oraz otwarty,
udokumentowany format. Może zostać także dostosowany do innych 
specyficznych wymagań.

%package desktop
Summary:	Graphical environment for plucker
Summary(pl.UTF-8):	Graficzne środowisko dla pluckera
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description desktop
This is the graphical environment for plucker.

%description desktop -l pl.UTF-8
To jest graficzne środowisko dla pluckera.

%prep
%setup -q
%patch -P1 -p0

%build
%define PyPluckerDir %{py_sitedir}/PyPlucker
%define DataDir %{_datadir}/%{name}
%define DocDir %{_datadir}/doc/%{name}-%{version}-%{release}

%{__gettextize}
%{__aclocal}
%{__autoconf}
%configure \
	--disable-palmosbuild \
	--with-wx-config=/usr/bin/wxgtk2-2.4-config

cp -f /usr/share/sgml-tools/epsf.sty /usr/share/latex2html/texinputs/html.sty docs
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

## Licence for palmosdk should be checked. Currently it is commented out.
## Viewer
#install -d $RPM_BUILD_ROOT%{DataDir}/palm
#install -m 755 viewer/*.prc $RPM_BUILD_ROOT%{DataDir}/palm
#install -m 755 viewer/*.pdb $RPM_BUILD_ROOT%{DataDir}/palm

#However, there still is a chance to poldek -i plucker-viewer-${LANG} ;-)

# Python Parser
install -d $RPM_BUILD_ROOT%{PyPluckerDir}/helper
install parser/python/PyPlucker/*.py $RPM_BUILD_ROOT%{PyPluckerDir}
install parser/python/PyPlucker/helper/*.py $RPM_BUILD_ROOT%{PyPluckerDir}/helper

# Config files
install -d $RPM_BUILD_ROOT%{DataDir}/config
install parser/defaults/exclusionlist.txt $RPM_BUILD_ROOT%{DataDir}/config
install parser/defaults/home.html $RPM_BUILD_ROOT%{DataDir}/config
install parser/defaults/pluckerrc.sample $RPM_BUILD_ROOT%{DataDir}/config

install -d $RPM_BUILD_ROOT%{_bindir}
sed -e "s:@VERSION@:%{version}:" \
	-e "s:@PLUCKERDIR@:%{DataDir}:" unix/setup.py.in > setup.py
install setup.py $RPM_BUILD_ROOT%{_bindir}/plucker-setup

# Documentation
# TODO: copy only needed files!
install -d manual
cp -rf docs/* manual

install -d $RPM_BUILD_ROOT%{_mandir}/man1
install docs/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

# desktop

install ./plucker_desktop/plucker-desktop $RPM_BUILD_ROOT%{_bindir}

for file in `ls ./plucker_desktop/resource`
do
	install -d $RPM_BUILD_ROOT%{DataDir}-desktop/resource/${file}
	install ./plucker_desktop/resource/${file}/* $RPM_BUILD_ROOT%{DataDir}-desktop/resource/${file}
done

# desktop - locale
for lang_ in `ls plucker_desktop/langs`
do
	if [ -f plucker_desktop/langs/${lang_}/plucker-desktop.mo ]; then
	install -d $RPM_BUILD_ROOT%{_datadir}/locale/${lang_}/LC_MESSAGES
	install plucker_desktop/langs/${lang_}/plucker-desktop.mo \
		$RPM_BUILD_ROOT%{_datadir}/locale/${lang_}/LC_MESSAGES
	fi
done

%find_lang plucker-desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(644,root,root,755)
%doc AUTHORS BUGREPORT CREDITS ChangeLog FAQ NEWS README REQUIREMENTS manual
%attr(755,root,root) %{_bindir}/plucker-setup
%{py_sitedir}/PyPlucker
%{_datadir}/plucker
%{_mandir}/man1/*.1*

%files desktop -f plucker-desktop.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/plucker-desktop
%{DataDir}-desktop/resource
