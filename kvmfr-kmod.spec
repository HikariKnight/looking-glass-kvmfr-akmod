%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%global tag master
%global ref heads
%endif

Name:     kvmfr-kmod
Version:  {{{ git_dir_version }}}
Release:  1%{?dist}
Summary:  Kvm framebuffer relay module for use with looking-glass
License:  GPLv2
URL:      https://github.com/gnif/LookingGlass

Source:   %{url}/archive/refs/%{ref}/%{tag}.tar.gz

# Fix for Kernel 6.13, remove when merged
# https://github.com/gnif/LookingGlass/pull/1149
Patch0:   https://patch-diff.githubusercontent.com/raw/gnif/LookingGlass/pull/1149.patch

BuildRequires: kmodtool
BuildRequires: patch

%description
Kvm framebuffer relay module for use with looking-glass

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%prep
%setup -q -c LookingGlass-%{tag}/module

find . -type f -name '*.c' -exec sed -i "s/#VERSION#/%{version}/" {} \+

%patch 0 -p1 -d LookingGlass-%{tag}

for kernel_version  in %{?kernel_versions} ; do
  cp -a LookingGlass-%{tag}/module _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/kvmfr.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/kvmfr.ko
done
%{?akmod_install}

%changelog
{{{ git_dir_changelog }}}
