%define	major	3
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

Summary:	A freely licensed alternative to the GLUT library
Name:		freeglut
Version:	2.8.0
Release:	5
License:	MIT
Group:		System/Libraries
URL:		http://freeglut.sourceforge.net
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# For the manpages
Source1:	http://downloads.sourceforge.net/openglut/openglut-0.6.3-doc.tar.gz
Patch0:		freeglut-2.8.0-fixXInput.patch
Patch1:		freeglut-2.8.0-btnmask.patch
Patch2:		freeglut-2.8.0-glextconflict.patch
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(ice)
# The virtual Provides below is present so that this freeglut package is a
# drop in binary replacement for "glut" which will satisfy rpm dependancies
# properly.  The Obsoletes tag is required in order for any pre-existing
# "glut" package to be removed and replaced with freeglut when upgrading to
# freeglut.  Note: This package will NOT co-exist with the glut package.

%description
freeglut is a completely open source alternative to the OpenGL Utility Toolkit
(GLUT) library with an OSI approved free software license. GLUT was originally
written by Mark Kilgard to support the sample programs in the second edition
OpenGL 'RedBook'. Since then, GLUT has been used in a wide variety of practical
applications because it is simple, universally available and highly portable.

freeglut allows the user to create and manage windows containing OpenGL
contexts on a wide range of platforms and also read the mouse, keyboard and
joystick functions.

%package -n	%{libname}
Summary:	A freely licensed alternative to the GLUT library
Group:		System/Libraries
Provides:	glut = 3.7
Obsoletes:	glut < 3.7
Conflicts:	%{mklibname mesaglut 3}
%rename		%{_lib}glut3

%description -n	%{libname}
freeglut is a completely open source alternative to the OpenGL Utility Toolkit
(GLUT) library with an OSI approved free software license. GLUT was originally
written by Mark Kilgard to support the sample programs in the second edition
OpenGL 'RedBook'. Since then, GLUT has been used in a wide variety of practical
applications because it is simple, universally available and highly portable.

freeglut allows the user to create and manage windows containing OpenGL
contexts on a wide range of platforms and also read the mouse, keyboard and
joystick functions.

%package -n %{devname}
Summary:	Freeglut developmental libraries and header files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	glut-devel = 3.7
Obsoletes:	glut-devel < 3.7
Provides:	%{name}-devel = %{version}-%{release}
Requires:	pkgconfig(glu)

%description -n %{devname}
Developmental libraries and header files required for developing or compiling
software which links to the freeglut library, which is an open source
alternative to the popular GLUT library, with an OSI approved free software
license.


%prep
%setup -q -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# (TV) fix build:
./autogen.sh
# --disable-warnings -> don't add -Werror to CFLAGS
%configure --disable-static --disable-warnings
%make

# (TV) fix permissions:
chmod -x doc/*.png doc/*.html

%install
%makeinstall_std

mkdir -p %{buildroot}%{_mandir}/man3
install -p -m644 doc/man/*.3 %{buildroot}%{_mandir}/man3

# We take the soname as the version because the package
# version doesn't really match -- the last release of
# the original glut was 3.7, and we need to match/exceed
# its version number.
VER=`ls %{buildroot}%{_libdir}/libglut.so.?.?.? |sed -e 's,.*\.so\.,,'`
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cat >%{buildroot}%{_libdir}/pkgconfig/glut.pc <<EOF
prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/GL

Name: glut
Description: GL Utility Toolkit
Requires: gl
Version: $VER
Libs: -lglut
Cflags: -I\${includedir}
EOF

%files -n %{libname}
%doc AUTHORS ChangeLog COPYING NEWS README TODO doc/*.png doc/*.html
# don't include contents of doc/ directory as it is mostly obsolete
%{_libdir}/libglut*.so.%{major}
%{_libdir}/libglut*.so.%{major}.*

%files -n %{devname}
%{_includedir}/GL/*.h
%{_libdir}/libglut.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%changelog
* Sun Apr 01 2012 Bernhard Rosenkraenzer <bero@bero.eu> 2.8.0-2
+ Revision: 788576
- Add a "glut" pkgconfig file - the old Mesa GLUT did, and we want
  to be a full drop-in replacement

* Tue Jan 17 2012 Alexander Khrukin <akhrukin@mandriva.org> 2.8.0-1
+ Revision: 761958
- version update 2.8.0

* Sat Nov 26 2011 Александр Казанцев <kazancas@mandriva.org> 2.6.0-1
+ Revision: 733600
- imported package freeglut

  + Paulo Ricardo Zanoni <pzanoni@mandriva.com>
    - Prevent accidents for now
    - imported package freeglut



* Thu Sep 15 2011 fwang <fwang> 2.6.0-6.mga2
+ Revision: 144028
- fix group
- add req on mesaglu as freeglut_std.h requires GL/glu.h

  + ahmad <ahmad>
    - The -devel package should provide '%%{name}-devel' (mga#2257)

* Wed Apr 20 2011 misc <misc> 2.6.0-4.mga1
+ Revision: 89134
- add a Requires on the library, not on main package
- remove explicit requires on -devel, as we have automated requires for that

* Tue Apr 19 2011 tv <tv> 2.6.0-3.mga1
+ Revision: 88822
- move Provides/Obsoletes/Conflicts into lib subpackage

* Tue Apr 19 2011 tv <tv> 2.6.0-2.mga1
+ Revision: 88460
- explicitely conflicts with %%libmesaglut3

* Tue Apr 19 2011 tv <tv> 2.6.0-1.mga1
+ Revision: 88413
- imported package freeglut

