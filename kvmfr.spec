%if 0%{?fedora}
%global debug_package %{nil}
%endif

Name:     kvmfr
Version:  B7~rc1
Release:  1%{?dist}
Summary:  Kvm framebuffer relay module for use with looking-glass
License:  GPLv2
URL:      https://github.com/HikariKnight/looking-glass-kvmfr-akmod

Source:   %{url}/archive/refs/heads/main.tar.gz

Provides: %{name}-kmod-common = %{version}
Requires: %{name}-kmod >= %{version}

BuildRequires: systemd-rpm-macros

%description
Kvm framebuffer relay module for use with looking-glass

%prep
%setup -q -c looking-glass-kvmfr-akmod-main

%build
install -D -m 0644 looking-glass-kvmfr-akmod-main/%{name}.conf %{buildroot}%{_modulesloaddir}/%{name}.conf

%files
%doc looking-glass-kvmfr-akmod-main/README.md
%license looking-glass-kvmfr-akmod-main/LICENSE
%{_modulesloaddir}/%{name}.conf

%changelog
{{{ git_dir_changelog }}}
