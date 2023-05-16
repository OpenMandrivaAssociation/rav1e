%define major 0
%define libname %mklibname rav1e %{major}
%define devname %mklibname -d rav1e
%define staticname %mklibname -d -s rav1e

%global optflags %{optflags} -O3

Name:		rav1e
Version:	0.6.6
Release:	1
Summary:	The fastest and safest AV1 encoder
License:	BSD
Group:		System/Libraries
URL:		https://github.com/xiph/rav1e
Source0:	https://github.com/xiph/rav1e/archive/%{version}/%{name}-%{version}.tar.gz
# Due to the fact that the Rust system crates is garbage and cannot normally be maintained in distributions, we need to change system of compilation.
# That's why from now on (until its creators wise up) we use vendored crates.
# It's a dirty way, but the only sensible one in the current situation.
Source1:	vendor.tar.xz

BuildRequires:	rust
BuildRequires:	rust-src
BuildRequires:	cargo
BuildRequires:	cargo-c
BuildRequires:	cmake
BuildRequires:	git-core
BuildRequires:	perl-interpreter
BuildRequires:	perl(Getopt::Long)
BuildRequires:	nasm
BuildRequires:	pkgconfig(aom)
BuildRequires:	pkgconfig(dav1d)

%description
rav1e is an experimental AV1 video encoder. It is designed to eventually cover 
all use cases, though in its current form it is most suitable for cases where 
libaom (the reference encoder) is too slow.

%package -n %{libname}
Summary:	The rav1e AV1 encoding library
Group:		System/Libraries

%description -n %{libname}
The rav1e AV1 encoding library.

%package -n %{devname}
Summary:	Development files for the rav1e AV1 encoding library
Group:		Development/Other
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files for the rav1e AV1 encoding library.

%package -n %{staticname}
Summary:	Static library files for the rav1e AV1 encoding library
Group:		Development/Other
Requires:	%{devname} = %{EVRD}

%description -n %{staticname}
Static library files for the rav1e AV1 encoding library.

%prep
%autosetup -a1 -p1

install -d -m 0755 .cargo
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'
[source.vendored-sources]
directory = './vendor'
[term]
verbose = true
EOF
rm -f Cargo.lock

# Disable rav1e_js
sed -i 's/"rav1e_js", //' Cargo.toml

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
%{_libdir}/librav1e.so.%{major}*

%files -n %{devname}
%{_includedir}/rav1e
%{_libdir}/librav1e.so
%{_libdir}/pkgconfig/rav1e.pc

%files -n %{staticname}
%{_libdir}/librav1e.a
