###############################################################################
#                                                                             #
#            PLEASE DON'T SUBMIT THIS PACKAGE TO MAIN/RELEASE YET!            #
#                                                                             #
###############################################################################
Really.

%define major 3
%define libfreeglut %mklibname freeglut %major
%define libfreeglut_devel %mklibname freeglut -d
%define libfreeglut_static_devel %mklibname freeglut -d -s

# For conflicting purposes:
# - mesaglut-devel has its "major" in the package name
# - there's no mesaglut-static-devel
%define libmesaglut %mklibname mesaglut 3
%define libmesaglut_devel %{libmesaglut}-devel

Name:      freeglut
Version:   2.6.0
Release:   %mkrel 1

License:   MIT
URL:       http://freeglut.sourceforge.net
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source0:   %{name}-%{version}.tar.gz

BuildRequires: libglu-devel

#------------------------------------------------------------------------------#

# package freeglut

Summary: OpenSourced OpenGL Utility Toolkit (GLUT) library
Group:   Development/C

%description
freeglut is a completely OpenSourced alternative to the OpenGL Utility Toolkit
(GLUT) library. GLUT was originally written by Mark Kilgard to support the
sample programs in the second edition OpenGL 'RedBook'. Since then, GLUT has
been used in a wide variety of practical applications because it is simple,
widely available and highly portable.

GLUT (and hence freeglut) allows the user to create and manage windows
containing OpenGL contexts on a wide range of platforms and also read the
mouse, keyboard and joystick functions.

#------------------------------------------------------------------------------#

%package -n %{libfreeglut}

Summary: OpenSourced OpenGL Utility Toolkit (GLUT) library
Group:   Development/C

Provides: %{name} = %{version}-%{release}

Conflicts: %{libmesaglut}

%description -n %{libfreeglut}
freeglut is a completely OpenSourced alternative to the OpenGL Utility Toolkit
(GLUT) library. GLUT was originally written by Mark Kilgard to support the
sample programs in the second edition OpenGL 'RedBook'. Since then, GLUT has
been used in a wide variety of practical applications because it is simple,
widely available and highly portable.

GLUT (and hence freeglut) allows the user to create and manage windows
containing OpenGL contexts on a wide range of platforms and also read the
mouse, keyboard and joystick functions.

%files -n %{libfreeglut}
%defattr(-,root,root)
%{_libdir}/libglut.so.%{major}
%{_libdir}/libglut.so.%{major}.*

#------------------------------------------------------------------------------#

%package -n %{libfreeglut_devel}

Summary: Development files for %{libfreeglut}
Group:   Development/C

Requires: %{libfreeglut} = %{version}-%{release}
Provides: lib%{name}-devel = %{version}-%{release}
Provides: libglut-devel = %{version}-%{release}

Conflicts: %{libmesaglut}-devel

%description -n %{libfreeglut_devel}
Development files for %{libfreeglut}

%files -n %{libfreeglut_devel}
%defattr(-,root,root)
%{_libdir}/libglut.so
%{_libdir}/libglut.la
%{_includedir}/GL/freeglut.h
%{_includedir}/GL/freeglut_ext.h
%{_includedir}/GL/freeglut_std.h
%{_includedir}/GL/glut.h

#------------------------------------------------------------------------------#

%package -n %{libfreeglut_static_devel}

Summary: Static development files for %{libfreeglut}
Group:   Development/C

Requires: %{libfreeglut_devel} = %{version}-%{release}
Provides: lib%{name}-static-devel = %{version}-%{release}
Provides: libglut-static-devel = %{version}-%{release}

%description -n %{libfreeglut_static_devel}
Static development files for %{libfreeglut}

%files -n %{libfreeglut_static_devel}
%defattr(-,root,root)
%{_libdir}/libglut.a

#------------------------------------------------------------------------------#

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}
