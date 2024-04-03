%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

Name:     kvmfr-kmod
Version:  B7-rc1
Release:  1%{?dist}
Summary:  Kvm framebuffer relay module for use with looking-glass
License:  GPLv2
URL:      https://github.com/gnif/LookingGlass

Source:   %{url}/archive/refs/tags/%{version}.tar.gz

BuildRequires: kmodtool

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }
