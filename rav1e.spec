%define debug_package %{nil}

Name:           rav1e
Version:        0.1.0
Release:        1
Summary:        The fastest and safest AV1 encoder

License:        BSD
URL:            https://github.com/xiph/rav1e
Source0:        https://github.com/xiph/rav1e/archive/0.1.0/%{name}-%{version}.tar.gz

BuildRequires:  rust
BuildRequires:  rust-src
BuildRequires:  cargo
BuildRequires:  cmake
BuildRequires:  git-core
BuildRequires:  perl-interpreter
BuildRequires:  perl(Getopt::Long)
BuildRequires:  nasm

%description
rav1e is an experimental AV1 video encoder. It is designed to eventually cover 
all use cases, though in its current form it is most suitable for cases where 
libaom (the reference encoder) is too slow.

%prep
%autosetup
#git submodule update --init

%build
cargo build --release

%install
mkdir -p %{buildroot}%{_bindir}
cp target/release/rav1e %{buildroot}%{_bindir}

%files
%doc README.md
%license LICENSE PATENTS
%{_bindir}/rav1e
