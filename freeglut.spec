%define major 3
%define libname %mklibname %name %major
%define develibname %mklibname -d %name

Summary:        A freely licensed alternative to the GLUT library
Name:           freeglut
Version:        2.6.0
Release:        %mkrel 6
URL:            http://freeglut.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# For the manpages
Source1:        http://downloads.sourceforge.net/openglut/openglut-0.6.3-doc.tar.gz
License:        MIT
Group:          System/Libraries
BuildRequires:  pkgconfig mesaglu-devel libxext-devel libxxf86vm-devel
BuildRequires:  libxi-devel libice-devel
# The virtual Provides below is present so that this freeglut package is a
# drop in binary replacement for "glut" which will satisfy rpm dependancies
# properly.  The Obsoletes tag is required in order for any pre-existing
# "glut" package to be removed and replaced with freeglut when upgrading to
# freeglut.  Note: This package will NOT co-exist with the glut package.

# Fix linking of the examples -- we don't package them, they just need to
# compile and link
Patch0: freeglut-2.6.0-fixld.patch
Patch1: freeglut-2.6.0-noxwarn.patch

%description
freeglut is a completely open source alternative to the OpenGL Utility Toolkit
(GLUT) library with an OSI approved free software license. GLUT was originally
written by Mark Kilgard to support the sample programs in the second edition
OpenGL 'RedBook'. Since then, GLUT has been used in a wide variety of practical
applications because it is simple, universally available and highly portable.

freeglut allows the user to create and manage windows containing OpenGL
contexts on a wide range of platforms and also read the mouse, keyboard and
joystick functions.

%package -n %libname
Summary:        A freely licensed alternative to the GLUT library
Group:          System/Libraries
Provides:       glut = 3.7
Obsoletes:      glut < 3.7
Conflicts:	%mklibname mesaglut 3

%description -n %libname
freeglut is a completely open source alternative to the OpenGL Utility Toolkit
(GLUT) library with an OSI approved free software license. GLUT was originally
written by Mark Kilgard to support the sample programs in the second edition
OpenGL 'RedBook'. Since then, GLUT has been used in a wide variety of practical
applications because it is simple, universally available and highly portable.

freeglut allows the user to create and manage windows containing OpenGL
contexts on a wide range of platforms and also read the mouse, keyboard and
joystick functions.


%package -n %develibname
Summary:        Freeglut developmental libraries and header files
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Provides:       glut-devel = 3.7
Obsoletes:      glut-devel < 3.7
Provides:       %{name}-devel = %{version}-%{release}
Requires:	mesaglu-devel

%description -n %develibname
Developmental libraries and header files required for developing or compiling
software which links to the freeglut library, which is an open source
alternative to the popular GLUT library, with an OSI approved free software
license.


%prep
%setup -q -a 1
%patch0 -p1 -b .fixld
%patch1 -p1 -b .noxwarn

%build
# (TV) fix build:
./autogen.sh
# --disable-warnings -> don't add -Werror to CFLAGS
%configure --disable-static --disable-warnings
%make

# (TV) fix permissions:
chmod -x doc/*.png doc/*.html


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
rm $RPM_BUILD_ROOT/%{_libdir}/*.la

mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man3
install -p -m 644 doc/man/*.3 $RPM_BUILD_ROOT/%{_mandir}/man3


%clean
rm -rf $RPM_BUILD_ROOT


%files -n %libname
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README TODO doc/*.png doc/*.html
# don't include contents of doc/ directory as it is mostly obsolete
%{_libdir}/libglut*.so.%{major}
%{_libdir}/libglut*.so.%{major}.*

%files -n %develibname
%defattr(-,root,root,-)
%{_includedir}/GL/*.h
%{_libdir}/libglut.so
%{_mandir}/man3/*

