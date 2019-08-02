%define major 3
%define libname %mklibname glut %{major}
%define devname %mklibname -d glut
%define snapshot 20190713
%global optflags %{optflags} -O3

Summary:	A freely licensed alternative to the GLUT library
Name:		freeglut
Epoch:		1
Version:	3.0.0
Release:	4.%{snapshot}.1
License:	MIT
Group:		System/Libraries
Url:		http://freeglut.sourceforge.net
# git clone https://github.com/dcnieho/FreeGLUT.git -b git_master && cd FreeGLUT/freeglut/freeglut/
# git archive --prefix=freeglut-3.0.0/ --format=tar HEAD | xz > ../freeglut-3.0.0.tar.xz
Source0:	https://github.com/dcnieho/FreeGLUT/releases/%{name}-%{version}.tar.xz
#Source0:	https://datapacket.dl.sourceforge.net/project/freeglut/freeglut/3.0.0/freeglut-3.0.0.tar.gz
# For the manpages
Source1:	http://downloads.sourceforge.net/openglut/openglut-0.6.3-doc.tar.gz
Patch0:		freeglut-3.0.0-fix-cmakefiles.patch
Patch1:		freeglut-3.0.0-alt-fix_cmake_dir.patch
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(libglvnd)
BuildRequires:	cmake
BuildRequires:	ninja

%description
freeglut is a completely open source alternative to the OpenGL Utility Toolkit
(GLUT) library with an OSI approved free software license. GLUT was originally
written by Mark Kilgard to support the sample programs in the second edition
OpenGL 'RedBook'. Since then, GLUT has been used in a wide variety of practical
applications because it is simple, universally available and highly portable.

freeglut allows the user to create and manage windows containing OpenGL
contexts on a wide range of platforms and also read the mouse, keyboard and
joystick functions.

%package -n %{libname}
Summary:	A freely licensed alternative to the GLUT library
Group:		System/Libraries
# The virtual Provides below is present so that this freeglut package is a
# drop in binary replacement for "glut" which will satisfy rpm dependencies
# properly.  The Obsoletes tag is required in order for any pre-existing
# "glut" package to be removed and replaced with freeglut when upgrading to
# freeglut.  Note: This package will NOT co-exist with the glut package.
Provides:	glut = 3.7

%description -n %{libname}
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
Requires:	%{libname} = %{EVRD}
Requires:	pkgconfig(libglvnd)
Requires:	pkgconfig(glu)
Provides:	glut-devel = 3.7
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Developmental libraries and header files required for developing or compiling
software which links to the freeglut library, which is an open source
alternative to the popular GLUT library, with an OSI approved free software
license.

%prep
%autosetup -p1 -a 1
# We take the soname as the version because the package
# version doesn't really match -- the last release of
# the original glut was 3.7, and we need to match/exceed
# its version number.
sed -i -e 's/VERSION_MINOR/SO_MINOR/g' *.pc.in

%build
%cmake \
	-DOpenGL_GL_PREFERENCE=GLVND \
	-DFREEGLUT_REPLACE_GLUT:BOOL=ON \
	-DFREEGLUT_BUILD_STATIC_LIBS:BOOL=OFF \
	-G Ninja

%ninja_build

%install
%ninja_install -C build
# always install glut.h and freeglut.pc
install -m644 include/GL/glut.h %{buildroot}%{_includedir}/GL
ln -s glut.pc %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

mkdir -p %{buildroot}%{_mandir}/man3
install -p -m644 doc/man/*.3 %{buildroot}%{_mandir}/man3

%files -n %{libname}
# don't include contents of doc/ directory as it is mostly obsolete
%{_libdir}/libglut.so.%{major}*

%files -n %{devname}
%doc AUTHORS ChangeLog COPYING README doc/*.png doc/*.html
%{_includedir}/GL/*.h
%{_libdir}/libglut.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/FreeGLUT/*.cmake
%{_mandir}/man3/*
