#define debug_package %{nil}
%define libname %mklibname rav1e 0
%define devname %mklibname -d rav1e
%define staticname %mklibname -d -s rav1e

Name:           rav1e
Version:        0.3.3
Release:        1
Summary:        The fastest and safest AV1 encoder

License:        BSD
URL:            https://github.com/xiph/rav1e
Source0:        https://github.com/xiph/rav1e/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  rust
BuildRequires:  rust-src
BuildRequires:  cargo
BuildRequires:	cargo-c
BuildRequires:  cmake
BuildRequires:  git-core
BuildRequires:  perl-interpreter
BuildRequires:  perl(Getopt::Long)
BuildRequires:  nasm
BuildRequires:  pkgconfig(aom)

%description
rav1e is an experimental AV1 video encoder. It is designed to eventually cover 
all use cases, though in its current form it is most suitable for cases where 
libaom (the reference encoder) is too slow.

%package -n %{libname}
Summary:	The rav1e AV1 encoding library
Group:		Development/Libraries

%description -n %{libname}
The rav1e AV1 encoding library

%package -n %{devname}
Summary:	Development files for the rav1e AV1 encoding library
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files for the rav1e AV1 encoding library

%package -n %{staticname}
Summary:	Static library files for the rav1e AV1 encoding library
Requires:	%{devname} = %{EVRD}

%description -n %{staticname}
Static library files for the rav1e AV1 encoding library

%prep
%autosetup

%build
cargo build --release
cargo cbuild --release \
	--destdir=%{buildroot} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--includedir=%{_includedir} \
	--pkgconfigdir=%{_libdir}/pkgconfig

%install
cargo install --root %{buildroot}%{_prefix} --no-track --path .
cargo cinstall --release \
	--destdir=%{buildroot} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--includedir=%{_includedir} \
	--pkgconfigdir=%{_libdir}/pkgconfig

%files
%doc README.md
%license LICENSE PATENTS
%{_bindir}/rav1e

%files -n %{libname}
%{_libdir}/librav1e.so.*

%files -n %{devname}
%{_includedir}/rav1e
%{_libdir}/librav1e.so
%{_libdir}/pkgconfig/rav1e.pc

%files -n %{staticname}
%{_libdir}/librav1e.a
