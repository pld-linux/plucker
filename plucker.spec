Summary:	plucker is PalmOS conduit
Summary(pl):	plucker jest conduitem dla systemu PalmOS
Name:		plucker
Version:	1.4	
Release:	%{relyear}-%{relmonth}-%{relday}-%{relhour}m%{relminute}m%{relsecond}s
License:	GPL
Group:		X11/Aplications
Source0:	http://www.plkr.org/snapshots/%{name}_snapshot.tar.gz
URL:		http://www.plkr.org
#Patch0:		%{name}-sysconfdir.patch
BuildRequires:	python-modules
BuildRequires:	wxGTK2-devel
Requires:	python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		relyear 	2003
%define		relmonth	09
%define		relday		14
%define 	relhour		07
%define		relminute	02
%define		relsecond	01

%define		release		%{relyear}-%{relmonth}-%{relday}_%{relhour}h%{relminute}m%{relsecond}s

%description
Plucker is a suite of programs which provide an offline web browser for 
Palm OS handheld devices.

%description -l pl
Plucker jest zestawem programów, które udostêpniaj± offlinow± przegl±darkê 
dla urz±dzeñ przeno¶nych opartych o system Palm OS.

%prep
%setup -q -n %{name}_%{release}
%patch0 -p1

%build
cd kodilib/linux

%{__make} \
	CXX="%{__cxx}" \
	SDL_CFLAGS="%{rpmcflags} -D_REENTRANT" \
	X11INCLUDES="-I/usr/X11R6/include"

cd ../../kiki/linux

# try to detect python version
PYTHON_VER=""
[ -d "/usr/include/python2.2" ] && PYTHON_VER="2.2"
[ -d "/usr/include/python2.3" ] && PYTHON_VER="2.3"
[ "$PYTHON_VER" == "" ] && \
    echo "Unknown python version or python-devel not found!" \
    exit 1

%{__make} \
	CXX="%{__cxx}" \
	X11_INCLUDES="%{rpmcflags} -I/usr/X11R6/include" \
	GLLIBS="-L/usr/X11R6/lib -lglut -lGLU -lGL" \
	PYTHON_VERSION=$PYTHON_VER \
	PYTHONLIBS="\
	    /usr/lib/libpython$PYTHON_VER.so* -lutil \
            /usr/lib/python$PYTHON_VER/lib-dynload/math.so \
	    /usr/lib/python$PYTHON_VER/lib-dynload/time.so"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{py,sounds}

install kiki/linux/kiki $RPM_BUILD_ROOT%{_bindir}
install kiki/py/*.py $RPM_BUILD_ROOT%{_datadir}/%{name}/py
install kiki/py/*.cfg $RPM_BUILD_ROOT%{_datadir}/%{name}/py
install kiki/py/*.hsc $RPM_BUILD_ROOT%{_datadir}/%{name}/py
install kiki/py/*.rec $RPM_BUILD_ROOT%{_datadir}/%{name}/py
install kiki/sounds/*.{wav,mp3,aif{,f}} $RPM_BUILD_ROOT%{_datadir}/%{name}/sounds

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc kiki/{Readme.txt,Thanks.txt}
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
