%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%global tag B7-rc1
%global curl /bin/curl --location --fail --silent --output
%global tarball https://github.com/gnif/LookingGlass/archive/refs/tags/LookingGlass-%{tag}.tar.gz
%endif

Name:     kvmfr-kmod
Version:  B7~rc1
Release:  1%{?dist}
Summary:  Kvm framebuffer relay module for use with looking-glass
License:  GPLv2
URL:      https://github.com/gnif/LookingGlass

Source:   %{url}/archive/refs/tags/%{tag}.tar.gz

BuildRequires: kmodtool

%description
Kvm framebuffer relay module for use with looking-glass

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%prep
cd %{_sourcedir}
%{curl} %{_sourcedir}/LookingGlass-%{tag}.tar.gz %{tarball}
tar -xvzf LookingGlass-%{tag}.tar.gz
%setup -q -c LookingGlass-%{tag}/module

find . -type f -name '*.c' -exec sed -i "s/#VERSION#/%{version}/" {} \+

for kernel_version  in %{?kernel_versions} ; do
  cp -a LookingGlass-%{version} _kmod_build_${kernel_version%%___*}
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
