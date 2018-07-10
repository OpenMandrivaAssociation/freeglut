%define	major	3
%define	libname	%mklibname glut %{major}
%define	devname	%mklibname -d glut

Summary:	A freely licensed alternative to the GLUT library
Name:		freeglut
Epoch:		1
Version:	2.8.1
Release:	12
License:	MIT
Group:		System/Libraries
Url:		http://freeglut.sourceforge.net
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# For the manpages
Source1:	http://downloads.sourceforge.net/openglut/openglut-0.6.3-doc.tar.gz
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xxf86vm)
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

%description -n	%{libname}
freeglut is a completely open source alternative to the OpenGL Utility Toolkit
(GLUT) library with an OSI approved free software license. GLUT was originally
written by Mark Kilgard to support the sample programs in the second edition
OpenGL 'RedBook'. Since then, GLUT has been used in a wide variety of practical
applications because it is simple, universally available and highly portable.

freeglut allows the user to create and manage windows containing OpenGL
contexts on a wide range of platforms and also read the mouse, keyboard and
joystick functions.

%package -n	%{devname}
Summary:	Freeglut developmental libraries and header files
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	glut-devel = 3.7
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Developmental libraries and header files required for developing or compiling
software which links to the freeglut library, which is an open source
alternative to the popular GLUT library, with an OSI approved free software
license.

%prep
%setup -q -a 1

%build
# (TV) fix build:
./autogen.sh
# --disable-warnings -> don't add -Werror to CFLAGS
%configure \
	--disable-static \
	--disable-warnings
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
%{_libdir}/libglut.so.%{major}*

%files -n %{devname}
%{_includedir}/GL/*.h
%{_libdir}/libglut.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

