Summary:	plucker is PalmOS conduit
Summary(pl):	plucker jest conduitem dla systemu PalmOS
Name:		plucker
Version:	1.4	
Release:	%{relyear}%{relmonth}%{relday}%{relhour}m%{relminute}m%{relsecond}s
License:	GPL
Group:		X11/Aplications
Source0:	http://www.plkr.org/snapshots/%{name}_snapshot.tar.gz
# Source0-md5:	df2c29d380a29bc04550a92a79a1769f
URL:		http://www.plkr.org
#Patch0:                %{name}-sysconfdir.patch
BuildRequires:	gtk+2-devel
BuildRequires:	netpbm-progs
BuildRequires:	python-modules
BuildRequires:	wxGTK2-devel
Requires:	python
BuildRoot:	%{tmpdir}/%{name}-%{version}-%{release}-root-%(id -u -n)

%define		relyear 	2003
%define		relmonth	09
%define		relday		14
%define 	relhour		12
%define		relminute	01
%define		relsecond	33

%define		release		%{relyear}-%{relmonth}-%{relday}_%{relhour}h%{relminute}m%{relsecond}s

%description
Plucker increase the utility of your handheld device by letting you view
web pages and any document that can be converted to HTML or text. Plucker
has many advanced features including the ability to read web pages with
embedded images, an advanced find function, the ability to open an e-mail
form when tapping on mail-links in web documents, an impressive compression
ratio for the documents and an open, documented format. It can also be
customized for your specific needs.

%description -l pl
Plucker increase the utility of your handheld device by letting you view
web pages and any document that can be converted to HTML or text. Plucker
has many advanced features including the ability to read web pages with
embedded images, an advanced find function, the ability to open an e-mail
form when tapping on mail-links in web documents, an impressive compression
ratio for the documents and an open, documented format. It can also be
customized for your specific needs.
##########%configure --disable-palmosbuild

%prep
%setup -q -n %{name}_%{release}
#cp %{_sourcedir}/setup.py.in %{_builddir}/%{name}-%{version}
#%patch0 -p1

%build
rm -f missing
%{__gettextize}
%{__aclocal}
%{__autoconf}
cd unix
cat>>pld_install_answers<<EOF
/
/bin
y
/usr/share/%{name}
/usr/share/doc/%{name}-{%version}-%{release}
y
/var/spool/netcomics
y
n
y
EOF
./install-plucker < pld_install_answers


%install
rm -rf $RPM_BUILD_ROOT
%define PyPluckerDir %{_libdir}/python/site-packages/PyPlucker
%define DataDir %{_datadir}/plucker
%define DocDir %{_datadir}/doc/packages/plucker


# Viewer
mkdir -p %{buildroot}/%{DataDir}/palm
install -m 755 viewer/*.prc %{buildroot}/%{DataDir}/palm
install -m 755 viewer/*.pdb %{buildroot}/%{DataDir}/palm

# Python Parser
mkdir -p %{buildroot}/%{PyPluckerDir}/helper
install -m 755 parser/PyPlucker/*.py %{buildroot}/%{PyPluckerDir}
install -m 755 parser/PyPlucker/helper/*.py %{buildroot}/%{PyPluckerDir}/helper

# Config files
mkdir -p %{buildroot}/%{DataDir}/config
install -m 644 parser/exclusionlist.txt %{buildroot}/%{DataDir}/config
install -m 644 parser/home.html %{buildroot}/%{DataDir}/config
install -m 644 parser/pluckerrc.sample %{buildroot}/%{DataDir}/config

mkdir -p %{buildroot}/%{_bindir}
sed -e "s:@VERSION@:%{version}:" \
    -e "s:@PLUCKERDIR@:%{DataDir}:" setup.py.in > setup.py
install -m 755 setup.py %{buildroot}/%{_bindir}/plucker-setup

#Documentation
mkdir -p %{buildroot}/%{DocDir}/manual
install -m 644 docs/* %{buildroot}/%{DocDir}/manual

install -m 644 AUTHORS BUGREPORT COPYING CREDITS ChangeLog %{buildroot}/%{DocDir}
install -m 644 FAQ TODO NEWS README REQUIREMENTS %{buildroot}/%{DocDir}

mkdir -p %{buildroot}/%{_mandir}/man1/
install -m 644 parser/plucker-build.1 %{buildroot}/%{_mandir}/man1/
install -m 644 parser/plucker-decode.1 %{buildroot}/%{_mandir}/man1/
install -m 644 parser/plucker-dump.1 %{buildroot}/%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT


%post
%define PyPluckerDir %{_libdir}/python/site-packages/PyPlucker

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
%{_bindir}/plucker-setup
%doc %{_datadir}/doc/packages/plucker
%{_mandir}/man1/plucker-build*
%{_mandir}/man1/plucker-decode*
%{_mandir}/man1/plucker-dump*
%{_libdir}/python/site-packages/PyPlucker
%{_datadir}/plucker
